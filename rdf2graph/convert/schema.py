"""`configs/*.yaml` を型付きの設定オブジェクトへ変換する。

CLAUDE.md アーキテクチャ原則#1「設定ファイル駆動」の実体化。Phase 3以降の全モジュールは
このモジュールが返す`EndpointConfig`だけを介して`configs/*.yaml`の内容を参照し、
エンドポイント固有の値をコードに直接埋め込まない。
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml

_SUPPORTED_UNMATCHED_POLICIES = ("drop", "other")
_SUPPORTED_VECTORIZERS = ("hashing", "tfidf")


class ConfigError(ValueError):
    """`configs/*.yaml`の形式・値が不正な場合の例外。"""


@dataclass(frozen=True)
class SamplingConfig:
    """CLAUDE.md 決定事項#6の規模上限をエンドポイントごとに具体化したもの。"""

    max_nodes: int
    max_edges: int
    page_size: int
    seed: int


@dataclass(frozen=True)
class LabelConfig:
    """分類ラベルの根拠となる述語と、頻度上位何件をカテゴリとして採用するか。"""

    property: str
    top_k: int
    unmatched_policy: Literal["drop", "other"]


@dataclass(frozen=True)
class FeaturesConfig:
    """Phase 4のエッジ/特徴量自動発見（決定事項#23）のしきい値と、テキスト特徴量の設定。"""

    auto_discover: bool
    min_coverage: float
    max_properties: int
    text_properties: list[str]
    text_vectorizer: Literal["hashing", "tfidf"]


@dataclass(frozen=True)
class SplitConfig:
    train: float
    val: float
    test: float
    stratify: bool


@dataclass(frozen=True)
class EndpointConfig:
    """1エンドポイント分の`configs/*.yaml`を検証済みの形で表現する。"""

    endpoint: str
    target_class: str
    sampling: SamplingConfig
    label: LabelConfig
    features: FeaturesConfig
    split: SplitConfig


def _require(mapping: dict, key: str, context: str) -> object:
    if key not in mapping or mapping[key] is None:
        raise ConfigError(f"{context}: missing required key {key!r}")
    return mapping[key]


def load_config(path: Path | str) -> EndpointConfig:
    """`configs/*.yaml`を読み込み、検証済みの`EndpointConfig`を返す。

    値の欠落・型不整合・許容範囲外の値は`ConfigError`として送出する
    （CLAUDE.md アーキテクチャ原則#6「例外を握りつぶさない」）。
    """
    path = Path(path)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError(f"{path}: top-level YAML must be a mapping, got {type(raw).__name__}")

    endpoint = _require(raw, "endpoint", str(path))
    target_class = _require(raw, "target_class", str(path))
    if not isinstance(endpoint, str) or not endpoint:
        raise ConfigError(f"{path}: 'endpoint' must be a non-empty string")
    if not isinstance(target_class, str) or not target_class:
        raise ConfigError(
            f"{path}: 'target_class' must be a non-empty string (config not finalized yet?)"
        )

    sampling_raw = _require(raw, "sampling", str(path))
    sampling = SamplingConfig(
        max_nodes=int(_require(sampling_raw, "max_nodes", f"{path}:sampling")),
        max_edges=int(_require(sampling_raw, "max_edges", f"{path}:sampling")),
        page_size=int(_require(sampling_raw, "page_size", f"{path}:sampling")),
        seed=int(_require(sampling_raw, "seed", f"{path}:sampling")),
    )
    if sampling.max_nodes <= 0 or sampling.max_edges <= 0 or sampling.page_size <= 0:
        raise ConfigError(f"{path}: sampling.max_nodes/max_edges/page_size must be positive")

    label_raw = _require(raw, "label", str(path))
    unmatched_policy = str(_require(label_raw, "unmatched_policy", f"{path}:label"))
    if unmatched_policy not in _SUPPORTED_UNMATCHED_POLICIES:
        raise ConfigError(
            f"{path}: label.unmatched_policy={unmatched_policy!r} must be one of "
            f"{_SUPPORTED_UNMATCHED_POLICIES}"
        )
    label = LabelConfig(
        property=str(_require(label_raw, "property", f"{path}:label")),
        top_k=int(_require(label_raw, "top_k", f"{path}:label")),
        unmatched_policy=unmatched_policy,  # type: ignore[arg-type]
    )
    if label.top_k <= 0:
        raise ConfigError(f"{path}: label.top_k must be positive")

    features_raw = _require(raw, "features", str(path))
    text_vectorizer = str(_require(features_raw, "text_vectorizer", f"{path}:features"))
    if text_vectorizer not in _SUPPORTED_VECTORIZERS:
        raise ConfigError(
            f"{path}: features.text_vectorizer={text_vectorizer!r} must be one of "
            f"{_SUPPORTED_VECTORIZERS}"
        )
    text_properties = _require(features_raw, "text_properties", f"{path}:features")
    if not isinstance(text_properties, list) or not all(isinstance(p, str) for p in text_properties):
        raise ConfigError(f"{path}: features.text_properties must be a list of strings")
    features = FeaturesConfig(
        auto_discover=bool(_require(features_raw, "auto_discover", f"{path}:features")),
        min_coverage=float(_require(features_raw, "min_coverage", f"{path}:features")),
        max_properties=int(_require(features_raw, "max_properties", f"{path}:features")),
        text_properties=list(text_properties),
        text_vectorizer=text_vectorizer,  # type: ignore[arg-type]
    )
    if not (0.0 <= features.min_coverage <= 1.0):
        raise ConfigError(f"{path}: features.min_coverage must be within [0, 1]")
    if features.max_properties <= 0:
        raise ConfigError(f"{path}: features.max_properties must be positive")

    split_raw = _require(raw, "split", str(path))
    split = SplitConfig(
        train=float(_require(split_raw, "train", f"{path}:split")),
        val=float(_require(split_raw, "val", f"{path}:split")),
        test=float(_require(split_raw, "test", f"{path}:split")),
        stratify=bool(_require(split_raw, "stratify", f"{path}:split")),
    )
    if not (0.0 < split.train < 1.0 and 0.0 < split.val < 1.0 and 0.0 < split.test < 1.0):
        raise ConfigError(f"{path}: split.train/val/test fractions must each be within (0, 1)")
    total = split.train + split.val + split.test
    if abs(total - 1.0) > 1e-6:
        raise ConfigError(f"{path}: split.train+val+test must sum to 1.0, got {total}")

    return EndpointConfig(
        endpoint=endpoint,
        target_class=target_class,
        sampling=sampling,
        label=label,
        features=features,
        split=split,
    )
