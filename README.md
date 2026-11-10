# SPADE

Windows quick start.

Windows 11 x64, PowerShell, Internet. NVIDIA GPU with a CUDA 13.0-compatible driver. Printer online. Cloudflare access approved.

Python 3.11 and 3.12 supported. Replace `--python 3.12` to use 3.12 and `--python 3.11` to use 3.11.

**1. Install tools — Administrator PowerShell.**

```powershell
winget install --id astral-sh.uv -e
winget install --id Git.Git -e
winget install --id GitHub.GitLFS -e
winget install --id Cloudflare.cloudflared -e
winget install --id Microsoft.VCRedist.2015+.x64 -e
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

Close PowerShell. Reopen normally.

**2. Get the project.**

Clone the integration branch with Git LFS. All paths below start in the project folder.

```powershell
git lfs install
git clone --branch feature/rfdetr-integration https://github.com/Brysen-Ross/cs425_SPADE_System.git
cd cs425_SPADE_System
git lfs pull
```

| Model | Weights path |
| --- | --- |
| RF-DETR Medium576 | `checkpoints/rf-medium-576-e8-ema.pth` |
| YOLO | `scripts/Weights/SPADE_Spaghetti_Only-2/weights/best.pt` |

Demo video: `scripts/spaghetti_failure.mp4`.


```powershell
uv sync --locked --python 3.12 --managed-python --extra cuda
uv run --locked --extra cuda python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

uv installs Python and the locked GPU dependencies. Expected: `CUDA available: True`. Otherwise update the NVIDIA driver or use the CPU fallback below.

**3. Configure SSH — once.**

Open [the printer terminal](https://voron0.compute.magishira.dev). Sign in. Run `whoami`; use its result as `PI_USERNAME` below.

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.ssh" | Out-Null
notepad "$env:USERPROFILE\.ssh\config"
```

Add this block. Replace `PI_USERNAME`. Save as `config`; file type **All files**, no `.txt`.

```sshconfig
Host voron0
    HostName voron0.compute.magishira.dev
    User PI_USERNAME
    ProxyCommand cloudflared access ssh --hostname %h
    IdentityFile ~/.cloudflared/voron0.compute.magishira.dev-cf_key
    CertificateFile ~/.cloudflared/voron0.compute.magishira.dev-cf_key-cert.pub
```

**4. Authenticate. Open the camera + Moonraker tunnel.**

```powershell
cloudflared access ssh-gen --hostname voron0.compute.magishira.dev
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:7125:127.0.0.1:7125 -L 127.0.0.1:8081:127.0.0.1:8080 voron0
```

Complete browser login. Keep this terminal open.

**5. Verify — second PowerShell.**

```powershell
curl.exe --fail http://127.0.0.1:7125/printer/info
Start-Process http://127.0.0.1:8081/snapshot
```

Expected: printer JSON; camera image.

**6. Launch — PowerShell in the project folder.**

```powershell
uv run --locked --extra cuda spade --model rfdetr --weights checkpoints/rf-medium-576-e8-ema.pth --video scripts/spaghetti_failure.mp4 --confidence 0.3 --device cuda
```

Config: `spade.toml`. Custom URLs/paths: copy it to `spade.local.toml`, edit, add `--config spade.local.toml`.

Another MP4: add `--video "PATH_TO_VIDEO.mp4"`.


**YOLO instead:**

```powershell
uv run --locked --extra cuda spade --model yolo --weights scripts/Weights/SPADE_Spaghetti_Only-2/weights/best.pt --video scripts/spaghetti_failure.mp4 --confidence 0.75 --device cuda
```

Other checkpoint location: replace the `--weights` path. Permanent settings: `spade.local.toml`.

**CPU fallback — no compatible NVIDIA GPU:**

```powershell
uv sync --locked --python 3.12 --managed-python --extra cpu
uv run --locked --extra cpu spade --model rfdetr --weights checkpoints/rf-medium-576-e8-ema.pth --video scripts/spaghetti_failure.mp4 --confidence 0.3 --device cpu
```

**Later sessions:** repeat step 4, then launch. `Permission denied`: regenerate the SSH certificate.

`Broken pipe` or a closed tunnel: repeat step 4; refresh connections in **Live Camera**.



[Connection troubleshooting](printer_setup_and_config_files/remote_printer_setup_instructions.md)
