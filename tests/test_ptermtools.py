#!/usr/bin/env python

"""Tests for `pauls_term_tools` package."""

import unittest

from everett.manager import ListOf, config_override

from ptermtools.config import CONFIG
from ptermtools.git_repo_organizer.repo_organizer import (
    Repo,
    _dealias_shortcut,
    _is_shortcut,
)


class TestConfig(unittest.TestCase):
    """Tests for `pauls_term_tools` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    @config_override(CODE_DIR="${HOME}/Code")
    def test_basic_get(self):
        """Test something."""
        self.assertEqual("${HOME}/Code", CONFIG("CODE_DIR"))

    @config_override(
        shortcuts="gh=https://github.com, glawi=https://github.awi.de, gldkrz=https://gitlab.awi.de"
    )
    def test_shortcut_config(self):
        config_shortcuts = CONFIG("shortcuts", parser=ListOf(str, delimiter=", "))
        print(f"config_shortcuts detected: {config_shortcuts}")
        self.assertEqual(
            [
                "gh=https://github.com",
                "glawi=https://github.awi.de",
                "gldkrz=https://gitlab.awi.de",
            ],
            config_shortcuts,
        )

    def test_is_shortcut(self):
        self.assertTrue(_is_shortcut("gh:pgierz/dots"))
        self.assertFalse(_is_shortcut("https://pgierz/dots"))
        self.assertFalse(_is_shortcut("http://pgierz/dots"))
        self.assertFalse(
            _is_shortcut("blah://no/thing/is/here"),
        )
        self.assertRaises(
            ValueError, _is_shortcut, "blah://no/thing/is/here", raise_on_missing=True
        )

    def test_dealias_shortcut(self):
        self.assertEqual(
            _dealias_shortcut("gh:pgierz/dots"), "https://github.com/pgierz/dots"
        )
        self.assertRaises(ValueError, _dealias_shortcut, "total_crap")


class TestRepo(unittest.TestCase):
    def test_repo_creation(self):
        r = Repo(url="https://github.com/pgierz/dots.git")
        self.assertEqual(r.repo_name, "dots")
        self.assertEqual(r.path, f"{CONFIG('CODE_DIR')}/github.com/pgierz/dots")
        self.assertEqual(r._id[:6], "40ad78")
        r = Repo.from_db("https://github.com/pgierz/pass.git")
