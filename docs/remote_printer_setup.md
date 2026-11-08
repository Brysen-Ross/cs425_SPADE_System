# First Time Setup:

1. Install ssh and curl in ubuntu/wsl:

  sudo apt update
  sudo apt install -y openssh-client curl

2. Install Cloudflare client in ubuntu/wsl by pasting the following:

  sudo mkdir -p --mode=0755 /usr/share/keyrings
  curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg \
    | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

  echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' \
    | sudo tee /etc/apt/sources.list.d/cloudflared.list

  sudo apt update
  sudo apt install -y cloudflared

3. Find your Raspberry Pi SSH Username:
  
  Open the browser based voron terminal in a web browser enter:

    "voron0.compute.magishira.dev" 

  authenticate through cloudflare access.

  Once logged in run the command "whoami" in the terminal. This will be needed for the next steps.

4. Create an SSH config directory and open the config file:

  mkdir -p ~/.ssh
  chmod 700 ~/.ssh
  nano ~/.ssh/config

5. Add the following in the SSH configuration file:
  NOTE: Change [INSERT USERNAME] with what "whoami" returned

  Host voron0
      HostName voron0.compute.magishira.dev
      User [INSERT USERNAME]

  Match host voron0.compute.magishira.dev exec "/usr/bin/cloudflared access ssh-gen --hostname %h"
      ProxyCommand /usr/bin/cloudflared access ssh --hostname %h
      IdentityFile ~/.cloudflared/%h-cf_key
      CertificateFile ~/.cloudflared/%h-cf_key-cert.pub

6. Test the Raspberry Pi SSH Connection by pasting the following in ubuntu/wsl:

  "ssh voron0"

  This should print a url. Follow the URL and log in with discord and authorize if needed.

7. From local Ubuntu/WSL paste the following. This will connect to moonraker and crowsnest for the cameras:

  ssh -N \
    -L 127.0.0.1:7125:127.0.0.1:7125 \
    -L 127.0.0.1:8081:127.0.0.1:8080 \
    voron0

  Note: After running the command, the terminal will appear to do nothing. This is intended. To verify the connections open a second terminal and run the following commands:

  "curl http://127.0.0.1:7125/printer/info"

