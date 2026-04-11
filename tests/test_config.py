"""
Tests for CrawlerConfig location-aware path resolution
∰◊€π¿🌌∞
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch

from crawler_pixel8.config import CrawlerConfig, _resolve_hodie_path, _resolve_base_dir


class TestResolveHodiePath:
    """Tests for _resolve_hodie_path() priority chain"""

    def test_hodie_path_env_takes_priority(self, tmp_path):
        """HODIE_PATH env var overrides everything else"""
        with patch.dict(os.environ, {"HODIE_PATH": str(tmp_path), "HODIE_LOCATION": "pixel8a"}):
            result = _resolve_hodie_path()
        assert result == tmp_path

    def test_pixel8a_location_returns_hardcoded_path(self):
        """HODIE_LOCATION=pixel8a returns the pixel8a path when HODIE_PATH is absent"""
        clean_env = {k: v for k, v in os.environ.items() if k != "HODIE_PATH"}
        clean_env["HODIE_LOCATION"] = "pixel8a"
        with patch.dict(os.environ, clean_env, clear=True):
            result = _resolve_hodie_path()
        assert result == Path("/storage/emulated/0/pixel8a/Q/hodie")

    def test_fallback_to_cwd_when_no_env(self):
        """Falls back to Path.cwd() when no relevant env vars are set"""
        clean_env = {k: v for k, v in os.environ.items()
                     if k not in ("HODIE_PATH", "HODIE_LOCATION")}
        with patch.dict(os.environ, clean_env, clear=True):
            result = _resolve_hodie_path()
        assert result == Path.cwd()

    def test_unknown_location_falls_back_to_cwd(self):
        """HODIE_LOCATION with an unrecognized value falls back to cwd"""
        clean_env = {k: v for k, v in os.environ.items() if k != "HODIE_PATH"}
        clean_env["HODIE_LOCATION"] = "mulberry"
        with patch.dict(os.environ, clean_env, clear=True):
            result = _resolve_hodie_path()
        assert result == Path.cwd()


class TestResolveBaseDir:
    """Tests for _resolve_base_dir() priority chain"""

    def test_q_root_env_takes_priority(self, tmp_path):
        """Q_ROOT env var overrides everything else"""
        with patch.dict(os.environ, {"Q_ROOT": str(tmp_path), "HODIE_LOCATION": "pixel8a"}):
            result = _resolve_base_dir()
        assert result == tmp_path

    def test_pixel8a_location_returns_hardcoded_path(self):
        """HODIE_LOCATION=pixel8a returns the pixel8a Q root"""
        clean_env = {k: v for k, v in os.environ.items() if k != "Q_ROOT"}
        clean_env["HODIE_LOCATION"] = "pixel8a"
        with patch.dict(os.environ, clean_env, clear=True):
            result = _resolve_base_dir()
        assert result == Path("/storage/emulated/0/pixel8a/Q")

    def test_fallback_to_cwd_when_no_env(self):
        """Falls back to Path.cwd() when no relevant env vars are set"""
        clean_env = {k: v for k, v in os.environ.items()
                     if k not in ("Q_ROOT", "HODIE_LOCATION")}
        with patch.dict(os.environ, clean_env, clear=True):
            result = _resolve_base_dir()
        assert result == Path.cwd()


class TestCrawlerConfigEnvVars:
    """Tests for CrawlerConfig fields driven by environment variables"""

    def test_location_name_from_env_name(self, tmp_path):
        """location_name reads ENV_NAME env var"""
        with patch.dict(os.environ, {"ENV_NAME": "mulberry", "HODIE_PATH": str(tmp_path)}):
            config = CrawlerConfig(
                crawler_output=tmp_path / "out",
                patterns_dir=tmp_path / "out/patterns",
                maps_dir=tmp_path / "out/maps",
                summaries_dir=tmp_path / "out/summaries",
                exports_dir=tmp_path / "out/exports",
                quanta_dir=tmp_path / "quanta",
            )
        assert config.location_name == "mulberry"

    def test_location_name_defaults_to_unknown(self, tmp_path):
        """location_name defaults to 'unknown' when ENV_NAME is absent"""
        clean_env = {k: v for k, v in os.environ.items()
                     if k not in ("ENV_NAME", "HODIE_PATH", "HODIE_LOCATION")}
        with patch.dict(os.environ, clean_env, clear=True):
            config = CrawlerConfig(
                crawler_output=tmp_path / "out",
                patterns_dir=tmp_path / "out/patterns",
                maps_dir=tmp_path / "out/maps",
                summaries_dir=tmp_path / "out/summaries",
                exports_dir=tmp_path / "out/exports",
                quanta_dir=tmp_path / "quanta",
            )
        assert config.location_name == "unknown"

    def test_max_concurrent_from_hq_max_concurrent(self, tmp_path):
        """max_concurrent reads HQ_MAX_CONCURRENT env var"""
        with patch.dict(os.environ, {"HQ_MAX_CONCURRENT": "8", "HODIE_PATH": str(tmp_path)}):
            config = CrawlerConfig(
                crawler_output=tmp_path / "out",
                patterns_dir=tmp_path / "out/patterns",
                maps_dir=tmp_path / "out/maps",
                summaries_dir=tmp_path / "out/summaries",
                exports_dir=tmp_path / "out/exports",
                quanta_dir=tmp_path / "quanta",
            )
        assert config.max_concurrent == 8

    def test_max_concurrent_defaults_to_3(self, tmp_path):
        """max_concurrent defaults to 3 (mobile device constraint)"""
        clean_env = {k: v for k, v in os.environ.items()
                     if k not in ("HQ_MAX_CONCURRENT", "HODIE_PATH", "HODIE_LOCATION")}
        with patch.dict(os.environ, clean_env, clear=True):
            config = CrawlerConfig(
                crawler_output=tmp_path / "out",
                patterns_dir=tmp_path / "out/patterns",
                maps_dir=tmp_path / "out/maps",
                summaries_dir=tmp_path / "out/summaries",
                exports_dir=tmp_path / "out/exports",
                quanta_dir=tmp_path / "quanta",
            )
        assert config.max_concurrent == 3

    def test_gemini_api_key_property(self, tmp_path):
        """gemini_api_key property reads GEMINI_API_KEY from env"""
        config = CrawlerConfig(
            crawler_output=tmp_path / "out",
            patterns_dir=tmp_path / "out/patterns",
            maps_dir=tmp_path / "out/maps",
            summaries_dir=tmp_path / "out/summaries",
            exports_dir=tmp_path / "out/exports",
            quanta_dir=tmp_path / "quanta",
        )
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key-123"}):
            assert config.gemini_api_key == "test-key-123"

    def test_gemini_api_key_none_when_absent(self, tmp_path):
        """gemini_api_key returns None when GEMINI_API_KEY is not set"""
        config = CrawlerConfig(
            crawler_output=tmp_path / "out",
            patterns_dir=tmp_path / "out/patterns",
            maps_dir=tmp_path / "out/maps",
            summaries_dir=tmp_path / "out/summaries",
            exports_dir=tmp_path / "out/exports",
            quanta_dir=tmp_path / "quanta",
        )
        clean_env = {k: v for k, v in os.environ.items() if k != "GEMINI_API_KEY"}
        with patch.dict(os.environ, clean_env, clear=True):
            assert config.gemini_api_key is None


class TestCrawlerConfigPaths:
    """Tests for CrawlerConfig output path derivation"""

    def test_output_paths_under_hodie_dir(self, tmp_path):
        """When HODIE_PATH is set, output paths resolve under it by default"""
        with patch.dict(os.environ, {"HODIE_PATH": str(tmp_path)}):
            config = CrawlerConfig()
        assert config.crawler_output == tmp_path / "crawler_output"
        assert config.patterns_dir == tmp_path / "crawler_output/patterns"
        assert config.maps_dir == tmp_path / "crawler_output/maps"
        assert config.summaries_dir == tmp_path / "crawler_output/summaries"
        assert config.exports_dir == tmp_path / "crawler_output/exports"
        assert config.quanta_dir == tmp_path / "quanta"

    def test_hodie_dir_set_from_hodie_path_env(self, tmp_path):
        """hodie_dir is resolved from HODIE_PATH env var"""
        with patch.dict(os.environ, {"HODIE_PATH": str(tmp_path)}):
            config = CrawlerConfig()
        assert config.hodie_dir == tmp_path

    def test_base_dir_set_from_q_root_env(self, tmp_path):
        """base_dir is resolved from Q_ROOT env var"""
        with patch.dict(os.environ, {"Q_ROOT": str(tmp_path), "HODIE_PATH": str(tmp_path / "hodie")}):
            config = CrawlerConfig(
                crawler_output=tmp_path / "hodie/out",
                patterns_dir=tmp_path / "hodie/out/patterns",
                maps_dir=tmp_path / "hodie/out/maps",
                summaries_dir=tmp_path / "hodie/out/summaries",
                exports_dir=tmp_path / "hodie/out/exports",
                quanta_dir=tmp_path / "hodie/quanta",
            )
        assert config.base_dir == tmp_path

    def test_conversation_archive_defaults_to_cwd(self, tmp_path):
        """conversation_archive defaults to Path.cwd() when not specified"""
        with patch.dict(os.environ, {"HODIE_PATH": str(tmp_path)}):
            config = CrawlerConfig()
        assert config.conversation_archive == Path.cwd()

    def test_directories_are_created(self, tmp_path):
        """__post_init__ creates all output directories"""
        with patch.dict(os.environ, {"HODIE_PATH": str(tmp_path)}):
            config = CrawlerConfig()
        assert config.crawler_output.is_dir()
        assert config.patterns_dir.is_dir()
        assert config.maps_dir.is_dir()
        assert config.summaries_dir.is_dir()
        assert config.exports_dir.is_dir()
        assert config.quanta_dir.is_dir()


class TestCrawlerConfigPostInit:
    """Tests for __post_init__ error handling"""

    def test_permission_error_does_not_raise(self, tmp_path):
        """PermissionError during mkdir is handled gracefully (no crash)"""
        with patch.dict(os.environ, {"HODIE_PATH": str(tmp_path)}):
            with patch("pathlib.Path.mkdir", side_effect=PermissionError("no access")):
                # Should not raise
                config = CrawlerConfig()
        assert config is not None

    def test_os_error_does_not_raise(self, tmp_path):
        """Non-PermissionError OSError during mkdir is handled gracefully"""
        with patch.dict(os.environ, {"HODIE_PATH": str(tmp_path)}):
            with patch("pathlib.Path.mkdir", side_effect=OSError("disk full")):
                config = CrawlerConfig()
        assert config is not None


class TestCrawlerConfigMethods:
    """Tests for CrawlerConfig helper methods"""

    def test_get_conversation_paths_finds_json(self, tmp_path):
        """get_conversation_paths() finds JSON files in the specified directory"""
        (tmp_path / "conv.json").write_text("[]", encoding="utf-8")
        config = CrawlerConfig(
            conversation_archive=tmp_path,
            crawler_output=tmp_path / "out",
            patterns_dir=tmp_path / "out/patterns",
            maps_dir=tmp_path / "out/maps",
            summaries_dir=tmp_path / "out/summaries",
            exports_dir=tmp_path / "out/exports",
            quanta_dir=tmp_path / "quanta",
        )
        paths = config.get_conversation_paths()
        assert any(p.name == "conv.json" for p in paths)

    def test_get_conversation_paths_search_dir_override(self, tmp_path):
        """get_conversation_paths() uses search_dir when provided"""
        subdir = tmp_path / "sub"
        subdir.mkdir()
        (subdir / "talk.md").write_text("# Hi", encoding="utf-8")
        config = CrawlerConfig(
            conversation_archive=tmp_path,
            crawler_output=tmp_path / "out",
            patterns_dir=tmp_path / "out/patterns",
            maps_dir=tmp_path / "out/maps",
            summaries_dir=tmp_path / "out/summaries",
            exports_dir=tmp_path / "out/exports",
            quanta_dir=tmp_path / "quanta",
        )
        paths = config.get_conversation_paths(search_dir=subdir)
        assert any(p.name == "talk.md" for p in paths)

    def test_get_entity_folders_returns_dirs_only(self, tmp_path):
        """get_entity_folders() returns only directories under quanta_dir"""
        quanta = tmp_path / "quanta"
        quanta.mkdir()
        (quanta / "tardigradia").mkdir()
        (quanta / "microversa").mkdir()
        (quanta / "notes.md").write_text("x", encoding="utf-8")
        config = CrawlerConfig(
            conversation_archive=tmp_path,
            crawler_output=tmp_path / "out",
            patterns_dir=tmp_path / "out/patterns",
            maps_dir=tmp_path / "out/maps",
            summaries_dir=tmp_path / "out/summaries",
            exports_dir=tmp_path / "out/exports",
            quanta_dir=quanta,
        )
        folders = config.get_entity_folders()
        names = {f.name for f in folders}
        assert names == {"tardigradia", "microversa"}

    def test_get_entity_folders_empty_when_no_quanta(self, tmp_path):
        """get_entity_folders() returns [] when quanta_dir does not exist"""
        config = CrawlerConfig(
            conversation_archive=tmp_path,
            crawler_output=tmp_path / "out",
            patterns_dir=tmp_path / "out/patterns",
            maps_dir=tmp_path / "out/maps",
            summaries_dir=tmp_path / "out/summaries",
            exports_dir=tmp_path / "out/exports",
            quanta_dir=tmp_path / "nonexistent_quanta",
        )
        assert config.get_entity_folders() == []
