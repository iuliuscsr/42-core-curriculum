*This project has been created as part of the 42 curriculum by jmalsam.*

# Born2beRoot

## Description

Born2beRoot is a system administration project from the 42 curriculum. The goal of the project is to introduce the fundamentals of virtualization, server administration, system security, and Linux configuration.

The project consists of creating and configuring a secure server inside a virtual machine. The system has to follow a set of strict rules concerning partitioning, user management, password policies, SSH, firewall configuration, sudo, and system monitoring.

For this project, **Debian** was chosen as the operating system and **Oracle VirtualBox** was used as the hypervisor.

The project was completed without the bonus part.

---

## Instructions

### Virtual Machine

The server is installed inside an **Oracle VirtualBox** virtual machine.

The operating system used is **Debian**. The installation is performed without a graphical interface, as required by the subject.

The hostname of the virtual machine follows the required 42 naming convention:

```text
jmalsam42
```

### SSH

SSH is configured to listen on port **4242**.

For security reasons, direct SSH login as `root` is disabled. The regular `jmalsam` user must be used for remote access.

Example:

```bash
ssh jmalsam@<IP_ADDRESS> -p 4242
```

### Firewall

The Debian installation uses **UFW (Uncomplicated Firewall)**.

The firewall is configured to be active at system startup and only allows the SSH service on port `4242`.

The status can be checked with:

```bash
sudo ufw status
```

### Users and Groups

A regular user named `jmalsam` is present in addition to the `root` user.

The required groups are:

* `sudo`
* `user42`

The user can be checked with:

```bash
groups jmalsam
```

### Password Policy

A strong password policy is configured using PAM.

The required PAM modules were installed and configured to enforce the password requirements specified by the subject.

The policy includes:

* Password expiration every 30 days.
* Minimum of 2 days between password changes.
* Warning 7 days before expiration.
* Minimum password length of 10 characters.
* At least one uppercase letter.
* At least one lowercase letter.
* At least one number.
* No more than 3 consecutive identical characters.
* The password must not contain the username.
* Password history requirements.

The configuration was implemented using the appropriate PAM configuration files and modules.

### Sudo

`sudo` is configured according to the security requirements of the subject.

The configuration includes:

* A maximum of 3 authentication attempts.
* A custom error message for incorrect passwords.
* Logging of sudo commands.
* Logging of sudo input and output.
* TTY mode enabled.
* Restricted paths available through sudo.

Sudo logs are stored in:

```text
/var/log/sudo/
```

### AppArmor

**AppArmor** is enabled and configured to start automatically with the system.

AppArmor provides mandatory access control by restricting what applications and processes are allowed to access on the system.

Its status can be checked with:

```bash
sudo aa-status
```

### Monitoring

A Bash monitoring script is located at:

```text
/usr/local/bin/monitoring.sh
```

The script displays system information every 10 minutes using `wall`.

The information includes:

* Operating system architecture and kernel version.
* Number of physical CPUs.
* Number of virtual CPUs.
* RAM usage and utilization percentage.
* Disk usage and utilization percentage.
* CPU utilization.
* Date and time of the last reboot.
* LVM status.
* Number of active TCP connections.
* Number of logged-in users.
* IPv4 address and MAC address.
* Number of commands executed using `sudo`.

The script is automatically executed every 10 minutes using **cron**.

It can be executed manually with:

```bash
sudo /usr/local/bin/monitoring.sh
```

---

## Design Choices

### Operating System: Debian

**Debian** was chosen for this project because it provides a stable and well-documented Linux environment and is recommended by the subject for students who are new to system administration.

#### Advantages

* Stable and reliable.
* Large software repository.
* Extensive documentation and community support.
* Uses `apt` for straightforward package management.
* Good compatibility with server environments.
* AppArmor provides an additional security layer.

#### Disadvantages

* Packages can be older than those found in distributions focused on more recent software.
* Some system administration tasks require a deeper understanding of Linux configuration.
* The default installation prioritizes stability over having the latest software versions.

### Partitioning

The system uses encrypted partitions for the main filesystem and swap space.

The encrypted partitions are managed using **LVM**, providing flexibility for managing logical volumes while adding encryption to protect data stored on the virtual machine.

The root and swap partitions are encrypted.

### Security

Several security mechanisms were implemented as part of the project:

* SSH is restricted to port `4242`.
* Root login through SSH is disabled.
* UFW is enabled and restricts incoming connections.
* A strong password policy is enforced through PAM.
* Sudo access is restricted and logged.
* AppArmor is enabled.
* The system does not use a graphical interface.

These measures reduce the attack surface and help protect the server from unauthorized access.

---

## Comparisons

### Debian vs Rocky Linux

Both Debian and Rocky Linux are stable Linux distributions suitable for server environments.

**Debian** uses the Debian package ecosystem and `apt`/`dpkg`, while **Rocky Linux** is designed to be binary-compatible with Red Hat Enterprise Linux and uses tools such as `dnf` and RPM.

Debian was chosen because it is recommended by the subject for beginners and provides a relatively straightforward environment for learning system administration.

Rocky Linux is particularly useful when learning technologies and administration practices associated with the Red Hat ecosystem.

### AppArmor vs SELinux

Both AppArmor and SELinux provide mandatory access control.

**AppArmor** uses security profiles that define what applications are allowed to access. It is commonly considered easier to configure and understand because its rules are closely associated with individual applications.

**SELinux** uses a label-based security model and provides highly granular access control. It is powerful and widely used in enterprise environments, but can have a steeper learning curve.

Debian uses **AppArmor**, which was therefore used for this project.

### UFW vs firewalld

Both UFW and firewalld are firewall management tools.

**UFW (Uncomplicated Firewall)** provides a simple interface for configuring the underlying firewall and is commonly used on Debian-based systems.

**firewalld** provides a more dynamic firewall management system and is commonly associated with distributions such as Rocky Linux.

Since Debian was selected, **UFW** was used for this project.

### VirtualBox vs UTM

Both VirtualBox and UTM can be used to create and run virtual machines.

**Oracle VirtualBox** is a widely used virtualization platform with support for multiple operating systems and extensive configuration options.

**UTM** is particularly useful on Apple hardware, including systems using Apple Silicon, and provides virtualization through Apple's virtualization technologies.

**Oracle VirtualBox** was used for this project.

---

## Resources

The following resources were used to understand and configure the system:

* Debian documentation and manuals.
* Linux manual pages (`man`).
* Documentation for `apt` and `dpkg`.
* Documentation for SSH and `sshd`.
* UFW documentation.
* AppArmor documentation.
* Documentation for `sudo`.
* Documentation for `cron`.
* Bash documentation.
* Oracle VirtualBox documentation.

The project also required researching fundamental system administration concepts such as virtualization, partitions, LVM, encryption, SSH, firewalls, PAM, sudo, AppArmor, and cron as well as fundamental knowledge about how a Server works.

### AI Usage

AI was used as a learning and support tool during the project.

It was mainly used for:

* Explaining fundamental computer science and system administration concepts.
* Helping understand unfamiliar Linux concepts and terminology.
* Acting as a second-level error checker when troubleshooting configurations or commands.
* Helping identify potential mistakes and inconsistencies.
* Assisting with the creation and structure of this `README.md`.

AI was not used as a replacement for understanding the system. The configuration and commands were reviewed and tested in the virtual machine, and the underlying concepts were studied to be able to explain them during the evaluation.

---

## Bonus

The bonus part was **not implemented**.

Only the mandatory requirements of the Born2beRoot project were completed.
