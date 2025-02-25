%define name boa-constructor
%define version 0.6.1

Name: %{name}
Summary: Python IDE and wxPython GUI Builder
Version: %{version}
Release: 6
Group: Development/Python
# the source come from a .zip
Source: %{name}-%{version}.tar.bz2
# icons
Source1: %{name}.16.png.bz2
Source2: %{name}.32.png.bz2
Source3: %{name}.48.png.bz2
# man pages
Source4: %{name}.1.bz2
Source5: %{name}.desktop
# to remove a annoying message when looking at help.
Patch: %{name}.help.patch
Url: https://boa-constructor.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: perl desktop-file-utils
Requires: wxPythonGTK pychecker python
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
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

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
cp %{SOURCE5} $RPM_BUILD_ROOT/%{_datadir}/applications/


desktop-file-install --vendor="" \
        --remove-category="Development" \
        --remove-category="Debugger" \
        --remove-category="GUIDesigner" \
        --add-category="GNOME" \
        --add-category="GTK" \
        --add-category="Development" \
        --add-category="X-MandrivaLinux-MoreApplications-Development-DevelopmentEnvironments" \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

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

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root,0755)
%doc *.txt README.Mandriva
%{_bindir}/%{name}
%{_datadir}/%{name}/*
%dir %{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_mandir}/*/*

%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-5mdv2011.0
+ Revision: 616802
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 0.6.1-4mdv2010.0
+ Revision: 424664
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.6.1-3mdv2009.0
+ Revision: 243356
- rebuild
- drop old menu
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Oct 21 2007 Jérôme Soyer <saispo@mandriva.org> 0.6.1-1mdv2008.1
+ Revision: 100995
- fix
- Add BR
- Fix Menu
- Fix Menu
- Add files
- New release 0.6.1

  + Thierry Vignaud <tv@mandriva.org>
    - kill CVS reference in README.urpmi !!


* Thu Aug 11 2005 Michael Scherer <misc@mandriva.org> 0.4.4-1mdk
- New release 0.4.4
- mkrel
- remove patch1, integrated upstream
- fix #10676 and his clones
- adapt patch0
- fix menu

* Thu Jun 17 2004 Michael Scherer <misc@mandrake.org> 0.2.3-3mdk 
- rebuild with proper Vendor and other tags

* Wed Aug 20 2003 Michael Scherer <scherer.michael@free.fr> 0.2.3-2mdk 
- the preference directory have changed in the CVS version, patch to use the new settings
    ( thanks Cedric Delfosse )

* Wed Aug 20 2003 Michael Scherer <scherer.michael@free.fr> 0.2.3-1mdk
- first spec for Mandrake
- man pages from Debian ( thanks Cedric Delfosse )
- pngification of Debian icon
- use a patch from Debian to use homedir for help cache

