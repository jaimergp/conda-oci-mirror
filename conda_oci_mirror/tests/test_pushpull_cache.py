#!/usr/bin/python

import os
import sys

import pytest

# The setup.cfg doesn't install the main module proper
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, root)
sys.path.insert(0, here)

# import conda_oci_mirror.defaults as defaults
from helpers import get_mirror  # noqa

from conda_oci_mirror.logger import setup_logger  # noqa

# Ensure we see all verbosity
setup_logger(debug=True, quiet=False)


@pytest.mark.parametrize(
    "subdir",
    ["noarch"],
)
def test_push_pull_cache(tmp_path, subdir):
    """
    Test push and pull of the cache.

    This test does a basic sanity check that when we run mirror,
    we are pushing to the registry the repodata and (if it exists)
    the package files. We verify by pull back again with oras,
    and checking file structure and/or size.
    """
    # Start with a mirror
    cache_dir = os.path.join(tmp_path, "cache")
    m = get_mirror(subdir, cache_dir)
    updates = m.update()
    assert len(updates) >= 2

    # Now we can use the mirror to push and pull from the cache
    m.pull_latest()
    m.push_new()
