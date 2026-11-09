# First Time Setup:

## Requirements: 
- Windows
- PowerShell
- Git
- Python 3.12
- Github repo is cloned locally 
  
**NOTE:** All commands below should be run in Windows PowerShell unless otherwise stated

**NOTE:** If viewing this file in Visual Studio Code, press Ctrl + Shift + V to open the formatted preview 

  1. Install the required dependencies (as of 11/9/26)

      a. Run the following in PowerShell: `py -3.12 -m pip install ultralytics torch opencv-python pillow numpy mss requests PyYAML`

  2. Install Cloudflare Client and Verify

      a. To Install run the following in PowerShell: `winget install --id Cloudflare.cloudflared -e`

      b. To Verify run the following in PowerShell: `cloudflared --version`

      c. Should return something similar to: "cloudflared version 2026.10.7"

      d. After installation, close and reopen PowerShell if cloudflared is not recognized during part b

  3. Find your Raspberry Pi SSH Username
    
      a.  Open the [Voron0 Web Terminal](https://voron0.compute.magishira.dev) in your browser.

      b. Authenticate through Cloudflare Access.

      c. Once logged in run the following in the terminal: `whoami`
    
      d. Save the username as it will be needed in the future.

  4. Create the Windows SSH Configuration File

      a. In powershell create the ssh config directory: `New-Item -ItemType Directory -Force "$HOME\.ssh"`

      b. Open the SSH config file: `notepad "$HOME\.ssh\config"`

      c. If prompted to create a new file, select "Yes". Make sure the file is named "config" and not "config.txt"

  5. Add the following in the SSH configuration file and replace [INSERT USERNAME] with the username obtained in step 3, then save and close the file 

      ```
      Host voron0
          HostName voron0.compute.magishira.dev
          User [INSERT USERNAME]
          ProxyCommand cloudflared access ssh --hostname %h
          IdentityFile ~/.cloudflared/voron0.compute.magishira.dev-cf_key
          CertificateFile ~/.cloudflared/voron0.compute.magishira.dev-cf_key-cert.pub
      ```

  6. Generate Cloudflare SSH Credentials

      a. Run the following in PowerShell: `cloudflared access ssh-gen --hostname voron0.compute.magishira.dev`

      b. If prompted, authenticate through Cloudflare Access

      c. Once completed, Cloudflare should generate the SSH key and certificate needed to connect to the Raspberry Pi automatically

  7. Test the Raspberry Pi SSH Connection

      a. Run the following in Powershell: `ssh voron0`

      b. If prompted, follow the provided URL and authenticate through Cloudflare Acess

      c. A successful connection should open the Raspberry Pi's terminal

      d. To disconnect from the Raspberry Pi, run: `exit`

      **NOTE:** The Raspberry Pi must be powered on and connected to the network.

      **Troubleshooting: SSH Permission Denied (publickey)**
        If SSH returns "Permission denied (publickey)", the Cloudflare authentication session or SSH certificate may have expired.

        1. Refresh Cloudflare authentication by running the following in PowerShell: `cloudflared access login https://voron0.compute.magishira.dev` and authenticate through the browser if prompted

        2. Regenerate the SSH certificate by running the following in PowerShell: `cloudflared access ssh-gen --hostname voron0.compute.magishira.dev`

        3. Return to step 7a

# Connecting to Moonraker and Camera

## Requirements:

- Steps 1-7 above have been completed once.

1. Run the following in PowerShell: `ssh -N -L 127.0.0.1:7125:127.0.0.1:7125 -L 127.0.0.1:8081:127.0.0.1:8080 voron0`

      **NOTE:** This command establishes an SSH connection to the Raspberry Pi and forwards two ports:

      - Port 7125: Moonraker API for printer communication.
      - Port 8081: Camera stream through Crowsnest.

  2. After running the command, the terminal will appear to do nothing. This is expected. Keep the terminal open while using SPADE

  3. Open a second PowerShell terminal to verify the connections

      a. Test the Moonraker connection by running the following in the 2nd terminal: `curl.exe http://127.0.0.1:7125/printer/info`

      **NOTE:** A successful connection should return JSON containing printer information

      b. Verify the camera connection by opening the [Camera Preview](http://127.0.0.1:8081/stream) in your web browser.

      **NOTE:** A successful connection would result in you seeing the livefeed from the camera in your web browser

      **NOTE:** The SSH tunnel from step 1 of this section must be active while SPADE communicates with Moonaraker and the camera. If the terminal is closed or the connection is interrupted, repeat Step 1 to reestablish the connection

# Running SPADE

## Requirements:

- First-Time Setup has been completed.
- SPADE GitHub repository has been cloned locally.
- Python 3.12 and required dependencies are installed.
- SSH tunnel is active

1. Open Powershell and navigate to the SPADE repository directory

2. Run the following in PowerShell: `py -3.12 -m spade.main`

    **NOTE:** This should open the tkinter GUI and run all implemented functions