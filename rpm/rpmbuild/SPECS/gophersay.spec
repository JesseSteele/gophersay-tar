Name:           gophersay-tar
Version:        1.0.0
Release:        1%{?dist}
Summary:        The talking gopher

License:        GPL
URL:            https://github.com/JesseSteele/gophersay-tar
Source0:        gophersay.tar.xz

BuildArch:      noarch
BuildRequires:  go
Requires:       go

%description
Gopher talkback written in Go for Linux

%prep
%setup -q

%build
go build -o gophersay gophersay.go

%install
mkdir -p %{buildroot}/usr/bin
install -D -m 0755 gophersay %{buildroot}/usr/bin/gophersay

%files
/usr/bin/gophersay

%changelog
-------------------------------------------------------------------
Thu Jan 01 00:00:00 UTC 1970 codes@jessesteele.com
- Something started, probably with v1.0.0-1