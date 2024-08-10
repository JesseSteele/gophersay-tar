# gophersay
## The talking gopher
Gopher talkback written in Go for Linux

- Built on [gophersay](https://github.com/jessesteele/gophersay), using a `.tar.xz` tarball as source for the local compiler
- This may be useful as an example when needing to compile from a tarball that contains multiple files
- The package will be `gophersay-tar`, but the command installed to the system will still be `gophersay` just as from the [gophersay](https://github.com/jessesteele/gophersay) repository

## Create the simple Linux install package for `gophersay` (via `gophersay-tar` package)
This is a guide to create an installer package for the `gophersay` command on:
1. Arch (Manjaro, Black Arch, et al)

Working examples for each already resides in this repository

### Create and install the `gophersay-tar` package directly from this repo

| **Arch** :$ (& Manjaro, Black Arch)

```console
git clone https://github.com/JesseSteele/gophersay-tar.git
cd gophersay/arch
makepkg -si
```

- These instructions presume you can access [gophersay.go](https://github.com/JesseSteele/gophersay-tar/blob/main/gophersay.go) & [go.mod](https://github.com/JesseSteele/gophersay-tar/blob/main/go.mod)

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
mkdir -p arch/gophersay-1.0.0
cp gophersay-tar/gophersay.go arch/gophersay-1.0.0/
cp gophersay-tar/go.mod arch/gophersay-1.0.0/
cd arch
tar Jcf gophersay-1.0.0.tar.xz gophersay-1.0.0
```

2. Get the `sha256sum` hash
  - We presume in these instructions that the hash is `713302921d243411a9cc2061afe24ebb34f0c833293f166dad9f8b03b6fbc969`, but yours may be different

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
