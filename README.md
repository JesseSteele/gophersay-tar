# gophersay
## The talking gopher
Gopher talkback written in Go for Linux

- Built on [gophersay](https://github.com/jessesteele/gophersay), using a `.tar.xz` tarball as source for the local compiler
- This may be useful as an example when needing to compile from a tarball that contains multiple files
- The package will be `gophersay-tar`, but the command installed to the system will still be `gophersay` just as from the [gophersay](https://github.com/jessesteele/gophersay) repository

## Create the simple Linux install package for `gophersay` (via `gophersay-tar` package)
This is a guide to create an installer package for the `gophersay` command on:
1. Arch (Manjaro, Black Arch, et al)
2. Debian (Ubuntu, Kali, Mint, et al)

Working examples for each already resides in this repository

### Create and install the `gophersay-tar` package directly from this repo

| **Arch** :$ (& Manjaro, Black Arch)

```console
git clone https://github.com/JesseSteele/gophersay-tar.git
cd gophersay/arch
makepkg -si
```

| **Debian** :$ (& Ubuntu, Kali, Mint)

```console
git clone https://github.com/JesseSteele/gophersay-tar.git
cd gophersay/deb/build
sudo dpkg-buildpackage -us -uc
cd debian
dpkg-deb --build gophersay
sudo dpkg -i gophersay.deb
```

## Detailed instructions per architecture
Instructions explain each in detail to create these packages from scratch...

### Preparation
These installers use a `.tar.xz` tarball for the installation

1. Create the tarball
  - Create the `gophersay-1.0.0/` directory
  - Place [gophersay.go](https://github.com/JesseSteele/gophersay-tar/blob/main/gophersay.go) & [go.mod](https://github.com/JesseSteele/gophersay-tar/blob/main/go.mod) inside the `gophersay-1.0.0/` directory
  - Roll up the `gophersay-1.0.0.tar.xz` tarball from `gophersay-1.0.0/`
    - :$ `tar Jcf gophersay-1.0.0.tar.xz gophersay-1.0.0`

| **Create `.xz` tarball** :$ (`gophersay-1.0.0.tar.xz`)

```console
git clone https://github.com/JesseSteele/gophersay-tar
mkdir -p gophersay-1.0.0
cp gophersay-tar/gophersay.go gophersay-1.0.0/
cp gophersay-tar/go.mod gophersay-1.0.0/
cd arch
tar Jcf gophersay-1.0.0.tar.xz gophersay-1.0.0
```

2. Get the `sha256sum` hash
  - We presume in these instructions that the hash is `acb473e96cf351ad5f571161bd560bbfaee46b0c9c5d23508e7acc6d76bd14c3`, but yours may be different

| **Get the `sha256sum` hash** :$ (`gophersay-1.0.0.tar.xz`)

```console
sha256sum gophersay-1.0.0.tar.xz
```

- Alternatively, if you want to be 1992 and use larger tarballs, you can use `.gz`

| **Create `.gz` tarball** :$ (1992, larger `gophersay-1.0.0.tar.gz`)

```console
tar zcf gophersay-1.0.0.tar.gz gophersay-1.0.0
```

| **Get the `sha256sum` hash** :$ (1992, larger `gophersay-1.0.0.tar.gz`)

```console
sha256sum gophersay-1.0.0.tar.gz
```

3. Use this `.tar.xz` tarball and hash in the following instructions
- These files have already been placed in the root of the repository for your convenience
- The `sha256sum` hash is in the file `gophersay-1.0.0.tar.xz.sha256sum`
- You can check the hash from the rood of the repository with :$ `sha256sum -c gophersay-1.0.0.tar.xz.sha256sum`
  - Or for 1992, larger `.gz` :$ `sha256sum -c gophersay-1.0.0.tar.gz.sha256sum`

### I. Arch Linux Package (`gophersay-tar-1.0.0-1-x86_64.pkg.tar.zst`)
*Arch package directory structure:*

| **`arch/`** :

```
arch/
├─ gophersay-1.0.0.tar.xz
└─ PKGBUILD
```

- Create directory: `arch`
- In `arch/` create file: `PKGBUILD`

| **`arch/PKGBUILD`** :

```
# Maintainer: Jesse Steele <codes@jessesteele.com>
pkgname=gophersay-tar
_cmdname=gophersay  # Custom variable to keep script clean, "should" start with _
pkgver=1.0.0
pkgrel=1
pkgdesc="Gopher talkback written in Go for Linux"
url="https://github.com/JesseSteele/gophersay"
arch=('x86_64')     # Go is newer and may not work on older systems, so not 'any'
license=('GPL')
depends=('go')      # Depends on the 'go' package to build the binary
replaces=('gophersay' 'gophersay-git')
source=("$_cmdname-$pkgver.tar.xz")
sha256sums=('713302921d243411a9cc2061afe24ebb34f0c833293f166dad9f8b03b6fbc969')

build() {
  cd "$srcdir/$_cmdname-$pkgver"
  go build -o "$_cmdname" "$_cmdname.go"
}

package() {
  install -Dm755 "$srcdir/$_cmdname-$pkgver/$_cmdname" "$pkgdir/usr/bin/$_cmdname"
}
```

- Place file `gophersay-1.0.0.tar.xz` in the same directory as `PKGBUILD`
- Build package:
  - Navigate to directory `arch/`
  - Run this, then the package will be built, then installed with `pacman`:

| **Build & install Arch package** :$ (in one command)

```console
makepkg -si
```

- Use this to build and install in two steps:

| **Build, *then* install Arch package** :$ (first line produces the `.pkg.tar.zst` file for repos or manual install)

```console
makepkg
sudo pacman -U gophersay-tar-1.0.0-1-x86_64.pkg.tar.zst
```

- Special notes about Arch:
  - We don't need to resolve any dependencies, we can omit the `-s` flag with `makepkg`
    - This package only needs `bash` as a dependency, which should already be installed merely to execute the script
      - `depends=('bash')` is redundant and only serves as an example in `PKGBUILD`
  - The name of the directory containing the package files does not matter
  - `PKGBUILD` is the instruction file, not a directory as might be expected with other package builders
  - `makepkg` must be run from the same directory containing `PKGBUILD`
  - The `.pkg.tar.zst` file will appear inside the containing directory

| **Remove Arch package** :$ (optional)

```console
sudo pacman -R gophersay-tar
```

### II. Debian Package (`gophersay.deb`)
*Debian "**maintainer**" build directory structure:*

| **`deb/`** :

```
deb/
├─ debian/
│  ├─ compat
│  ├─ control
│  ├─ copyright
│  ├─ changelog
│  ├─ install
│  └─ rules
└─ gophersay-1.0.0.tar.xz
```

- Create directories: `deb/build/debian`
- In `debian/` create file: `control`

| **`deb/build/debian/control`** :

```
Source: gophersay
Section: games
Priority: optional
Maintainer: Jesse Steele <codes@jessesteele.com>
Homepage: https://github.com/JesseSteele/gophersay
Build-Depends: debhelper (>= 10), golang-go
Standards-Version: 3.9.6

Package: gophersay
Version: 1.0.0
Architecture: all
Depends: bash (>= 4.0)
Description: Gopher talkback written in Go for Linux
```

- In `debian/` create file: `compat`

| **`deb/build/debian/compat`** : (`debhelper` minimum version)

```
10
```

- In `debian/` create file: `changelog`

| **`deb/build/debian/changelog`** : (optional, for listing changes)

```
gophersay (1.0-1) stable; urgency=low

  * First release

 -- Jesse Steele <codes@jessesteele.com>  Thu, 1 Jan 1970 00:00:00 +0000
```

- In `debian/` create file: `copyright`

| **`deb/build/debian/copyright`** : (optional, may be legally wise)

```
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: gophersay
Source: https://github.com/JesseSteele/gophersay

Files: *
Copyright: 2024, Jesse Steele <codes@jessesteele.com>
License: GPL-3+
```

- In `debian/` create file: `rules`
  - Make it executable with :$ `chmod +x debian/rules`

| **`deb/build/debian/rules`** : (build compiler)

```
#!/usr/bin/make -f

%:
	dh $@

override_dh_auto_build:
  tar xf gophersay-1.0.0.tar.xz
	go build -o gophersay gophersay.go

override_dh_auto_install:
	install -D -m 0755 gophersay $(DESTDIR)/usr/bin/gophersay
```

- In `debian/` create file: `install`

| **`deb/build/debian/install`** : (places files in the `.deb` directory structure)

```
gophersay /usr/bin
```

- Place tarball `gophersay-1.0.0.tar.xz` at `deb/build/gophersay-1.0.0.tar.xz`
- Install the `dpkg-dev`, `debhelper` & `golang-go` packages

| **Install Debian `dpkg-dev` package** :$

```console
sudo apt-get update
sudo apt-get install dpkg-dev debhelper golang-go
```

- Prepare package builder:
  - Navigate to directory `deb/build/`
  - Run this, then the package builder & repo packages will be created:

| **Prepare the Debian package builder** :$

```console
sudo dpkg-buildpackage -us -uc  # Create the package builder
```

- Note what just happened
  - Everything just done to this point is called "**maintainer**" work in the Debian world
  - Basic repo packages *and also* the package `DEBIAN/` builder structure were greated
  - At this point, one could navigate up one directory to `deb/` and run `sudo dpkg -i gophersay_1.0-1_all.deb` and the package would be installed, *but we won't do this*
  - The command has also been created at `/usr/bin/gophersay`
    - Once installed with `sudo dpkg -i` (later) this can be removed the standard way with `sudo apt-get remove gophersay`
  - This is the new, just-created directory structure for the standard Debian package builder:

| **`deb/build/debian/`** :

```
deb/build/debian/
          └─ gophersay/
             ├─ DEBIAN/
             │  ├─ control
             │  └─ md5sums
             └─ usr/
                └─ bin/
                   └─ gophersay
```

- Build package:
  - Navigate to directory `deb/build/debian/`
    - :$ `cd debian`
  - Run this, then the package will be built, then installed:

| **Build, *then* install Debian package** :$

```console
dpkg-deb --build gophersay  # Create the .deb package
sudo dpkg -i gophersay.deb  # Install the package
```

- Special notes about Debian
  - The `deb/build/` directory can be anything, but we want it for housekeeping...
    - `dpkg-buildpackage` will create a laundry list of files as peers to this directory in `deb/`
  - The `debian/control` file builds `DEBIAN/control`, but uses different fields
    - Fields after the empty line in this `debian/control` example will not be recognized by the `dpkg-buildpackage` builder, but will supply information for `DEBIAN/control` in the final `.deb` package
  - The `rules` script will compile `gophersay` from `gophersay.go`
  - The `install` script will place the compiled `gophersay` binary at `usr/bin/gophersay` inside the package
    - This is why we don't need to place the binary at `usr/bin/gophersay` manually
  - Note `usr/local/bin/` won't work for CLI command files because Debian packages expect binary commands to go in `/usr/bin/`
    - Debian can install *directories*—but *cannot install any **file***—under `usr/local/`
    - Trying to install a file will return an [error from the package manager](https://unix.stackexchange.com/questions/409800/) since it expects directories, but only finds a file
  - The standard package build files (for `dpkg-deb --build`) will appear at `deb/build/debian/gophersay/DEBIAN/`
    - So from `deb/build/debian/` one could run `dpkg-deb --build gophersay` to create the `.deb` package at `deb/build/debian/gophersay.deb`
  - The standard package installer will appear at `deb/gophersay_1.0-1_all.deb`

| **Remove Debian package** :$ (optional)

```console
sudo apt-get remove gophersay
```