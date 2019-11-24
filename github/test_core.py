# Run these tests with "pytest github/test_core.py"

import json

from testtools import TestCase

from effect import ParallelEffects
from effect.testing import resolve_effect

from .core import get_orgs, get_org_repos, get_orgs_repos


class GithubTests(TestCase):
    def test_get_orgs_request(self):
        """
        get_orgs returns an effect that makes an HTTP request to
        the GitHub API to look up organizations for a user.
        """
        eff = get_orgs("radix")
        http = eff.intent
        self.assertEqual(http.method, "get")
        self.assertEqual(http.url, "https://api.github.com/users/radix/orgs")

    def test_get_orgs_success(self):
        """get_orgs extracts the result into a simple list of orgs."""
        eff = get_orgs("radix")
        self.assertEqual(
            resolve_effect(
                eff, json.dumps([{"login": "twisted"}, {"login": "rackerlabs"}])
            ),
            ["twisted", "rackerlabs"],
        )

    def test_get_org_repos_request(self):
        """
        get_org_repos returns an effect that makes an HTTP request to
        the GitHub API to look up repos in an org.
        """
        eff = get_org_repos("twisted")
        http = eff.intent
        self.assertEqual(http.method, "get")
        self.assertEqual(http.url, "https://api.github.com/orgs/twisted/repos")

    def test_get_org_repos_success(self):
        """get_org_repos extracts the result into a simple list of repos."""
        eff = get_org_repos("radix")
        self.assertEqual(
            resolve_effect(eff, json.dumps([{"name": "twisted"}, {"name": "txstuff"}])),
            ["twisted", "txstuff"],
        )

    def test_get_orgs_repos(self):
        """
        get_orgs_repos returns an Effect which looks up the organizations for
        a user, and then looks up all of the repositories of those orgs in
        parallel, and returns a single flat list of all repos.
        """
        effect = get_orgs_repos("radix")
        self.assertEqual(effect.intent.method, "get")
        self.assertEqual(effect.intent.url, "https://api.github.com/users/radix/orgs")
        next_effect = resolve_effect(
            effect, json.dumps([{"login": "twisted"}, {"login": "rackerlabs"}])
        )
        self.assertIsInstance(next_effect.intent, ParallelEffects)
        # Get each parallel effect
        effects = next_effect.intent.effects
        self.assertEqual(effects[0].intent.method, "get")
        self.assertEqual(
            effects[0].intent.url, "https://api.github.com/orgs/twisted/repos"
        )
        self.assertEqual(effects[1].intent.method, "get")
        self.assertEqual(
            effects[1].intent.url, "https://api.github.com/orgs/rackerlabs/repos"
        )
        self.assertEqual(
            resolve_effect(next_effect, [["twisted", "txstuff"], ["otter", "nova"]]),
            ["twisted", "txstuff", "otter", "nova"],
        )

    # These tests don't have 100% coverage, but they should teach you
    # everything you need to know to extend to testing any type of effect.
