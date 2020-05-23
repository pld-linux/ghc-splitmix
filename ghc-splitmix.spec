#
# Conditional build:
%bcond_without	prof	# profiling library
#
Summary:	splitmix: Fast Splittable PRNG
Name:		ghc-splitmix
Version:	0.0.4
Release:	0.1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/splitmix
Source0:	http://hackage.haskell.org/package/splitmix-%{version}/splitmix-%{version}.tar.gz
# Source0-md5:	a6d7539078d2c88de87f73756939dee4
URL:		http://hackage.haskell.org/package/splitmix
BuildRequires:	ghc
BuildRequires:	ghc-random
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-random-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires:	ghc-random
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Pure Haskell implementation of SplitMix described in

Guy L. Steele, Jr., Doug Lea, and Christine H. Flood. 2014.
Fast splittable pseudorandom number generators. In Proceedings of the
2014 ACM International Conference on Object Oriented Programming
Systems Languages & Applications (OOPSLA '14). ACM, New York, NY, USA,
453-472. DOI: https://doi.org/10.1145/2660193.2660195

%package prof
Summary:	Profiling splitmix library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca splitmix dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-random-prof

%description prof
Profiling splitmix library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca splitmix dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n splitmix-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/splitmix.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc Changelog.md LICENSE README.md %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/splitmix.conf
%dir %{_libdir}/%{ghcdir}/splitmix-%{version}
%{_libdir}/%{ghcdir}/splitmix-%{version}/libHSsplitmix-%{version}-*.so
%{_libdir}/%{ghcdir}/splitmix-%{version}/libHSsplitmix-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/splitmix-%{version}/libHSsplitmix-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/splitmix-%{version}/Data
%dir %{_libdir}/%{ghcdir}/splitmix-%{version}/Data/Bits
%{_libdir}/%{ghcdir}/splitmix-%{version}/Data/Bits/*.hi
%{_libdir}/%{ghcdir}/splitmix-%{version}/Data/Bits/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/splitmix-%{version}/System
%dir %{_libdir}/%{ghcdir}/splitmix-%{version}/System/Random
%{_libdir}/%{ghcdir}/splitmix-%{version}/System/Random/*.hi
%{_libdir}/%{ghcdir}/splitmix-%{version}/System/Random/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/splitmix-%{version}/libHSsplitmix-%{version}-*_p.a
%{_libdir}/%{ghcdir}/splitmix-%{version}/Data/Bits/*.p_hi
%{_libdir}/%{ghcdir}/splitmix-%{version}/System/Random/*.p_hi
%endif
