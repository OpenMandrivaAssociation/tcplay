%define major 3
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d
%define oldlibname %mklibname %{name} 3

Summary:	A free pretty much fully featured and stable TrueCrypt implementation
Name:		tcplay
Version:	3.3
Release:	2
License:	BSD and Public Domain
Group:		File tools
URL:		https://github.com/bwalex/tc-play
Source0:	https://github.com/bwalex/tc-play/archive/v%{version}/tc-play-%{version}.tar.gz
Patch0:		tc-play-3.3-fix-build.patch

BuildRequires:	cmake
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(openssl)

%description
tcplay is a free (BSD-licensed), pretty much fully featured (including multiple
keyfiles, cipher cascades, etc) and stable TrueCrypt implementation.

This implementation supports mapping (opening) both system and normal TrueCrypt
volumes, as well as opening hidden volumes and opening an outer volume while
protecting a hidden volume. There is also support to create volumes, including
hidden volumes, etc. Since version 1.1, there is also support for restoring
from the backup header (if present), change passphrase, keyfile and PBKDF2
PRF function.

Since tcplay uses dm-crypt (or dm_target_crypt on DragonFly) it makes full use
of any available hardware encryption/decryption support once the volume has
been mapped.

It is based solely on the documentation available on the TrueCrypt website,
many hours of trial and error and the output of the Linux' TrueCrypt client.
As it turns out, most technical documents on TrueCrypt contain mistakes, hence
the trial and error approach.

%files
%{_sbindir}/%{name}
%{_mandir}/man3/%{name}.3*
%{_mandir}/man8/%{name}.8*
%doc README.md
%doc CHANGELOG
%doc LICENSE

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	Primary library for %{name}
Group:		System/Libraries
Obsoletes:	%oldlibname < %{EVRD}

%description -n %{libname}
Primary library for %{name}.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%doc LICENSE

#--------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and static libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%{_includedir}/tcplay_api.h
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/*.pc
%doc CHANGELOG
%doc LICENSE

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n tc-play-%{version}

%build
%cmake
%make_build

%install
%make_install -C build

# remove static library
rm -fr %{buildroot}%{_libdir}/lib%{name}.a
