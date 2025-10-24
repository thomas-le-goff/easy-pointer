from fastapi import Depends
from typing import Annotated


from ..github.client import GitHubClient

GitHubClientDep = Annotated[GitHubClient, Depends(GitHubClient)]
