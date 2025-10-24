import asyncio
import shutil

from pathlib import Path

from .config import EditorSettings
from .schemas import EditorReadIn, EditorReadOut, EditorWriteIn, EditorWriteOut

from ..user.models import User


class CommandExecutionError(Exception):
    def __init__(self, cmd: str, returncode: int, stdout: str, stderr: str):
        self.cmd = cmd
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(
            f"Command '{cmd}' failed with code {returncode}: {stderr.strip() or stdout.strip()}")

# TODO use dispose pattern within DI


class CodeManager:

    workdir: Path

    def __init__(self, settings: EditorSettings, user: User, challenge='hello-world') -> None:
        self.settings = settings
        self.user = user
        self.challenge = challenge
        self.workdir = self.settings.work_storage_path / \
            str(self.user.id) / challenge
        self.challenge_template_dir = self.settings.template_path / challenge

    async def write(self, request: EditorWriteIn):
        response = EditorWriteOut(
            code=request.code, file_name=request.file_name)

        try:
            with (self.workdir / request.file_name).open('w') as f:
                f.write(request.code)
                f.close()
                try:
                    await self.build_challenge(force=True)
                except CommandExecutionError as error:
                    response.error = error.stderr
        except FileNotFoundError:
            response.error = "File not found"
        return response

    def read(self, request: EditorReadIn):
        response = EditorReadOut(code="", file_name=request.file_name)
        if not self.workdir.exists():
            if not self.challenge_template_dir.exists():
                raise Exception('Challenge not found')
            self.workdir.mkdir(parents=True)
            shutil.copytree(self.challenge_template_dir,
                            self.workdir, dirs_exist_ok=True)

        try:
            with (self.workdir / request.file_name).open() as f:
                s = f.read()
                response.code = s
        except FileNotFoundError:
            response.error = "File not found"
        return response

    async def render(self):
        try:
            await self.build_challenge(force=False)
        except CommandExecutionError as error:
            return error.stderr
        with (self.workdir / f'{self.challenge}.html').open() as f:
            s = f.read()
            return s

    async def build_challenge(self, force=False):
        if force or not (self.workdir / self.challenge).exists():
            await self.run(f'make -C {self.workdir}')
            await self.run(f'cd {self.workdir} && {self.settings.wasmfour_executable} bundle build/cart.wasm --title "My Game" --html {self.challenge}.html')

    async def run(self, cmd: str):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        if proc.returncode and proc.returncode != 0:
            raise CommandExecutionError(
                cmd, proc.returncode, stdout.decode(), stderr.decode())
        return stdout.decode()
