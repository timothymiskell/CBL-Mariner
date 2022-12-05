%{?python_enable_dependency_generator}
%global debug_package %{nil}

%global modname ssh2-python

Name:           python-%{modname}
Version:        0.27.0
Release:        1%{?dist}
Summary:        Super fast SSH library - bindings for libssh2
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ParallelSSH/ssh2-python
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/ssh2-python-%{version}.tar.gz
Source1:        conftest.py

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libssh2-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-Cython
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme

%if %{with_check}
BuildRequires:  openssh-clients
BuildRequires:  openssh-server
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif

%description
%{summary}.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
Requires:   python3

%description -n python3-%{modname}
%{summary}.

%prep
%autosetup -n %{modname}-%{version}
# No bundled libs
rm -vrf libssh2
sed -i -r 's:build_ssh2[(].*:pass:' setup.py
# Remove pre-generated sources
rm $(grep -rl '/\* Generated by Cython')

%build
export HAVE_AGENT_FWD=0
# use build_ext to completely instruct cythonize options
export CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}"
export LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}"
export CXXFLAGS="${CXXFLAGS:-${RPM_OPT_FLAGS}}"
python3 setup.py build_ext --inplace
python3 -msphinx -M html doc _build

%install
%py3_install

%check
# FIXME skip b0rken tests with segmentation fault from jinja2, rhbz#2007478
rm tests/test_knownhost.py tests/test_session.py tests/test_sftp.py
# FIXME skip another b0rken tests
rm tests/test_channel.py

# fake ssh-agent
eval `%{_bindir}/ssh-agent`
chmod 600 tests/unit_test_key
%{_bindir}/ssh-add tests/unit_test_key
chmod 600 tests/embedded_server/rsa.key
%{_bindir}/ssh-add tests/embedded_server/rsa.key
%{_bindir}/ssh-add -l

%{python3} -m pip install atomicwrites attrs docutils pluggy pygments six more-itertools
%pytest -v tests

%files -n python3-%{modname}
%license COPYING LICENSE
%doc README.rst Changelog.rst
%doc examples/ _build/html/
%{python3_sitearch}/ssh2_python-*.egg-info/

%changelog
* Wed Jun 22 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.27.0-1
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- Adding as run dependency for package cassandra medusa
- bump version to 0.27.0
- License verified

* Thu Sep 23 2021 Raphael Groner <raphgro@fedoraproject.org> - 0.26.0-1
- bump to v0.26.0
- generate and ship documentation incl. examples

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.15.0-12
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.15.0-9
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.0-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.0-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.15.0-3
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.15.0-1
- Initial package
