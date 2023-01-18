%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_moddir: %{expand: %%global _httpd_moddir %%{_libdir}/httpd/modules}}
%{!?_httpd_confdir: %{expand: %%global _httpd_confdir %{_sysconfdir}/httpd/conf.d}}

# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}

Name:		mod_auth_cookie_mysql2
Version:	1.1
Release:	1%{?dist}
Summary:	Mod Auth Cookie MySql2 module for Apache HTTP Server

License:	ASL 2.0
URL:		http://home.digithi.de/digithi/dev/mod_auth_cookie_mysql/
Source0:	http://home.digithi.de/digithi/dev/mod_auth_cookie_mysql/mod_auth_cookie_mysql2_%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	httpd-devel
BuildRequires:	mariadb-connector-c-devel
Requires:	httpd-mmn = %{_httpd_mmn}

%description
This module enables an Apache 2.x web server to do cookie authentication.

%prep
%setup -q

%build
# workaround rpm-buildroot-usage
export MODULES_DIR=%{_httpd_moddir}
export APXS2_OPTS='-S LIBEXECDIR=${MODULES_DIR}'

%{make_build}

%install
# workaround rpm-buildroot-usage
export MODULES_DIR=$RPM_BUILD_ROOT%{_httpd_moddir}
export APXS2_OPTS='-S LIBEXECDIR=${MODULES_DIR}'

mkdir -p $RPM_BUILD_ROOT%{_httpd_moddir}
make install

install -m 755 -d $RPM_BUILD_ROOT%{_httpd_modconfdir}
echo 'LoadModule auth_cookie_mysql2_module modules/mod_auth_cookie_mysql2.so' > \
	$RPM_BUILD_ROOT%{_httpd_modconfdir}/10-auth_cookie_mysql2.conf

install -m 755 -d $RPM_BUILD_ROOT%{_httpd_confdir}


%files
%doc INSTALL
%doc README
%{_httpd_moddir}/mod_auth_cookie_mysql2.so
%config(noreplace) %{_httpd_modconfdir}/10-auth_cookie_mysql2.conf

%changelog
* Wed Jan 18 2023 Thimo Eichstaedt <apache-mod@digithi.de> - 1.1-1
- Initial packaging for AlmaLinux
