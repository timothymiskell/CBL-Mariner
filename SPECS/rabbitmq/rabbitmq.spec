%define  debug_package %{nil}
Summary:        rabbitmq-server
Name:           rabbitmq-server
Version:        3.11.9
Release:        1%{?dist}
License:        Apache-2.0 and MPL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rabbitmq.com
Source0:        https://github.com/rabbitmq/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
BuildRequires:  erlang
BuildRequires:  elixir
BuildRequires:  libxslt
BuildRequires:  xmlto
BuildRequires:  python
BuildRequires:  python-simplejson
BuildRequires:  zip
BuildRequires:  unzip

%description
rabbitmq-server

%prep
%autosetup

%build
%make_build

%install
%make_install

%files
%license LICENSE


%changelog
* Tue Mar 14 2023 Sam Meluch <sammeluch@microsoft.com> - 3.11.9-1
- Original version for CBL-Mariner
- License Verified
