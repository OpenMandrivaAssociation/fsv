%define name fsv
%define version 0.9
%define release %mkrel 12

Name: %{name}
Version: %{version}
Release: %{release}
Group: File tools
License: LGPL
URL: http://fsv.sourceforge.net/
Summary: Fsv - 3D File System Visualizer
Source: %{name}-%{version}.tar.bz2
Buildrequires: gtk+-devel MesaGLU-devel glib-devel
Buildrequires: gtkglarea-devel 

%description
fsv (pronounced effessvee) is a file system visualizer in cyberspace. It
lays out files and directories in three dimensions, geometrically
representing the file system hierarchy to allow visual overview and
analysis. fsv can visualize a modest home directory, a workstation's hard
drive, or any arbitrarily large collection of files, limited only by the
host computer's memory and hardware constraints.

%prep

%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS"
# do not use macro, it doesn't work
./configure --prefix=%{_prefix}  --with-doc-dir=$RPM_DOC_DIR/%{name}-%{version}

%make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix} docdir=`pwd`/doc.rpm
mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig
install -m 644 fsv.wmconfig $RPM_BUILD_ROOT/etc/X11/wmconfig/fsv


(cd $RPM_BUILD_ROOT
mkdir -p ./%{_menudir}
cat > ./%{_menudir}/%{name} <<EOF
?package(%{name}):\
command="%{_bindir}/fsv"\
title="Fsv"\
longtitle="3D file browser"\
needs="x11"\
icon="file_tools_section.png"\
section="Applications/File tools"
EOF
)    

%post
%{update_menus}


%postun
%{clean_menus}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc.rpm/*
%config(noreplace) %{_sysconfdir}/X11/wmconfig/fsv
%{_bindir}/*
## %{prefix}/share/locale/*/*/*
%{_menudir}/*

