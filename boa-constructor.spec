%define name boa-constructor
%define version 0.4.4

Name: %{name}
Summary: Python IDE and wxPython GUI Builder
Version: %{version}
Release: %mkrel 1
Group: Development/Python
# the source come from a .zip
Source: %{name}-%{version}.tar.bz2
# icons
Source1: %{name}.16.png.bz2
Source2: %{name}.32.png.bz2
Source3: %{name}.48.png.bz2
# man pages
Source4: %{name}.1.bz2
# to remove a annoying message when looking at help.
Patch: %{name}.help.patch
Url: http://boa-constructor.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: perl
Requires: wxPythonGTK pychecker python
License: GPL
BuildArch: noarch

%description
Boa Constructor is a cross platform Python IDE and wxPython GUI Builder.
It offers visual frame creation and manipulation, an object inspector,
many views on the source like object browsers, inheritance hierarchies,
doc string generated html documentation, an advanced debugger
and integrated help.

Zope support: Object creation and editing. Cut, copy, paste,
import and export. Property creation and editing in the Inspector
and Python Script debugging.

%prep
%setup -q 

# (misc) dos2unix on all sources, and config since it is a software developed on windows
perl -pi -e 's%\r\n$%\n%' $(find . -name '*.py')
perl -pi -e 's%\r\n$%\n%' $(find . -name '*.cfg')
perl -pi -e 's%\r\n$%\n%' $(find . -name '*.txt')

%patch -p0

cat << EOF > README.Mandriva
This RPM incorporate a patch made by Cedric Delfosse, of Debian, to use the 
~/.boa-constructor directory to store the cache of help file.
EOF

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
echo -e "#!/bin/sh\npython %{_datadir}/%{name}/Boa.py" >  $RPM_BUILD_ROOT/%{_bindir}/%{name}
chmod +x $RPM_BUILD_ROOT/%{_bindir}/%{name}

mkdir -p $RPM_BUILD_ROOT/%{_menudir}/
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/%{name}
?package(%{name}): command="boa-constructor" \
needs="X11" section="Applications/Development/Development Environments" title="Boa-constructor" icon="%{name}.png" \
longtitle="Python IDE" 
EOF

install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}/
cp -Rf * $RPM_BUILD_ROOT/%{_datadir}/%{name}/

install -d $RPM_BUILD_ROOT/%{_miconsdir}
install -d $RPM_BUILD_ROOT/%{_iconsdir}
install -d $RPM_BUILD_ROOT/%{_liconsdir}
bunzip2 -c %{SOURCE1} >  $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
bunzip2 -c %{SOURCE2} >  $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
bunzip2 -c %{SOURCE3} >  $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png


install -d $RPM_BUILD_ROOT/%{_mandir}/man1/
bunzip2 -c %{SOURCE4} >  $RPM_BUILD_ROOT/%{_mandir}/man1/%{name}.1


# (misc) remove documentation
find $RPM_BUILD_ROOT/%{_datadir}/%{name}/ -maxdepth 1 -name '*.txt' | xargs rm -Rf 
rm -Rf $RPM_BUILD_ROOT/%{_datadir}/%{name}/README.Mandriva
%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root,0755)
%doc *.txt README.Mandriva
%{_bindir}/%{name}
%{_datadir}/%{name}/*
%dir %{_datadir}/%{name}/
%{_mandir}/*/*
%{_menudir}/%{name}

%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

