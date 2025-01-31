# Disable binary stripping due to premade binary (which
# other tools like dfhack will need to recognize by checksum).
%global debug_package %{nil}
%global __strip /bin/true

Name:           dwarffortress
Version:        0.47.05
Release:        6%{?dist}

Summary:        A single-player procedurally generated fantasy game

License:        Dwarf Fortress
URL:            http://www.bay12games.com/dwarves/

# Due to pre-compiled stuff, there is a separate 32 and 64 bit architecture.
Source0:        http://www.bay12games.com/dwarves/df_47_05_linux.tar.bz2

# The libgraphics sources, as maintained by the Arch Linux packager.
Source1:        https://github.com/svenstaro/dwarf_fortress_unfuck/archive/%{version}/dwarffortress-libgraphics-%{version}.zip

# Desktop file.
Source2:        dwarffortress.desktop

# Appstream file.
Source3:        dwarffortress.appdata.xml

# Launcher script.
Source4:        dwarffortress

# Icon.
Source5:        dwarffortress.png

# https://github.com/svenstaro/dwarf_fortress_unfuck/commit/6dcfe5ae869fddd51940c6c37a95f7bc639f4389
Patch0:         6dcfe5ae869fddd51940c6c37a95f7bc639f4389.patch

# Only build for 32 and 64 bit x86 systems.
# (According to kwizart, just use i686 here).
ExclusiveArch:  x86_64

# BuildRequires from https://github.com/svenstaro/dwarf_fortress_unfuck/
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  gcc-c++

# devel package BRs, sorted alphabetically (adapted from above link)
BuildRequires:  atk-devel
BuildRequires:  cairo-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glew-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk3-devel
BuildRequires:  libICE-devel
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel
BuildRequires:  libpng-devel
BuildRequires:  libSM-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  openal-soft-devel
BuildRequires:  pango-devel
BuildRequires:  ncurses-devel
BuildRequires:  SDL-devel
BuildRequires:  SDL_image-devel
BuildRequires:  SDL_ttf-devel

# BuildRequires we need for the packaging.
BuildRequires:  desktop-file-utils
BuildRequires:  dos2unix
BuildRequires:  libappstream-glib
BuildRequires:  unzip

%description
Dwarf Fortress is a single-player fantasy game. You can control a dwarven
outpost or an adventurer in a randomly generated, persistent world.

Although Dwarf Fortress is still in a work in progress, many features
have already been implemented.

Dwarf Fortress is free to redistribute, but is not open source.

%prep
tar xfj %SOURCE0

# Extract other sources.
cd df_linux/
unzip -qo %SOURCE1

# Fix some permissions.
find -type d -exec chmod 755 {} +
find -type f -exec chmod 644 {} +
dos2unix *.txt

cd dwarf_fortress_unfuck*
%patch -P0 -p1

%build
cd df_linux/dwarf_fortress_unfuck*

# Something in the default make flags prevents dfhack from linking to DF.
%cmake -DOpenGL_GL_PREFERENCE=GLVND
%cmake_build

%install
cd df_linux/
mkdir -p %{buildroot}%{_datadir}/dwarffortress/
mkdir -p %{buildroot}%{_libexecdir}/dwarffortress/
cp -ra data raw sdl %{buildroot}%{_datadir}/dwarffortress/

# Copy over the actual binary and compiled graphics library.
install -p -Dm755 libs/Dwarf_Fortress %{buildroot}%{_libexecdir}/dwarffortress/Dwarf_Fortress
install -p -Dm755 dwarf_fortress_unfuck*/%{_vpath_builddir}/libgraphics.so %{buildroot}%{_libexecdir}/dwarffortress/libgraphics.so
strip %{buildroot}%{_libexecdir}/dwarffortress/libgraphics.so

# Install .desktop file and launcher script from Arch Linux package.
# Or, rather, the modified versions.
install -p -Dm755 %SOURCE4 %{buildroot}%{_bindir}/dwarffortress
sed 's|prefix=/usr|prefix=%{_prefix}|' -i %{buildroot}%{_bindir}/dwarffortress
install -p -Dm644 %SOURCE2 %{buildroot}%{_datadir}/applications/dwarffortress.desktop
install -p -Dm644 %SOURCE5 %{buildroot}%{_datadir}/pixmaps/dwarffortress.png
desktop-file-validate %{buildroot}%{_datadir}/applications/dwarffortress.desktop

# Install appdata file and validate it.
mkdir -p %{buildroot}%{_metainfodir}/
cp -a %SOURCE3 %{buildroot}%{_metainfodir}/
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

%files
%doc df_linux/*.txt df_linux/README.linux
%{_datadir}/dwarffortress/
%{_libexecdir}/dwarffortress/
%{_bindir}/dwarffortress
%{_datadir}/applications/dwarffortress.desktop
%{_datadir}/pixmaps/dwarffortress.png
%{_metainfodir}/dwarffortress.appdata.xml

%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Tue Jul 19 2022 Leigh Scott <leigh123linux@gmail.com> - 0.47.05-1
- Updated to latest upstream release, 0.47.05.
- Apply upstream fix for rfbz#6368
- Use cmake macros
- Remove i686 support

* Mon Feb 28 2022 Sérgio Basto <sergio@serjux.com> - 0.47.04-6
- Rebuid for glew-2.2.0

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.47.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.47.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.47.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Ben Rosser <rosser.bjr@gmail.com> - 0.47.04-1
- Updated to latest upstream release, 0.47.04.

* Mon Feb 24 2020 Ben Rosser <rosser.bjr@gmail.com> - 0.47.03-1
- Update to latest upstream release.

* Fri Jan 31 2020 Chris Collins <collins.christopher@gmail.com> - 0.47.01-1
- Updated to latest upstream release.

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.44.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.44.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 30 2018 Sérgio Basto <sergio@serjux.com> - 0.44.12-2
- Rebuild for glew 2.1.0

* Thu Aug 09 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.12-1
- Updated to latest upstream release.

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 0.44.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.11-1
- Updated to latest upstream version, 0.44.11.

* Thu May 24 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.10-1
- Updated to latest upstream version, 0.44.10.
- Add the launcher files separately as individual sources, not a tarball.
- Fix a bug in the desktop file.

* Mon Apr 09 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.09-1
- Update to latest upstream release.

* Thu Mar 15 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.07-1
- Updated to latest upstream release.

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.44.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Ben Rosser <rosser.bjr@gmail.com> 0.44.05-1
- Updated to latest upstream release.

* Fri Jan 12 2018 Ben Rosser <rosser.bjr@gmail.com> 0.44.04-1
- Updated to latest upstream release.

* Tue Dec 26 2017 Ben Rosser <rosser.bjr@gmail.com> 0.44.03-1
- Updated to latest upstream release.

* Wed Nov 29 2017 Ben Rosser <rosser.bjr@gmail.com> 0.44.02-1
- Updated to latest upstream release.
- Update URL for dwarffortress launcher.

* Mon Aug 07 2017 Ben Rosser <rosser.bjr@gmail.com> 0.43.05-6
- Write and include AppData metadata file for Dwarf Fortress.
- Use macros for cmake and make when compiling.
- Sort BRs alphabetically, remove mesa-* BRs in favor of vendor-agnostic version.
- Use cp -a and install -p to preserve timestamps when copying.

* Thu Aug 03 2017 Ben Rosser <rosser.bjr@gmail.com> 0.43.05-5
- Clean up spec file, removing several commented out bits.
- Use better syntax to disable stripping/debug package since DF is a prebuilt binary.
- Clean up buildrequires, put them each on a separate line.

* Wed Feb 01 2017 Ben Rosser <rosser.bjr@gmail.com> 0.43.05-4
- Remove explicit dependency on alsa-plugins-pulseaudio, as it is no longer needed.

* Fri Jan 20 2017 Ben Rosser <rosser.bjr@gmail.com> 0.43.05-3
- Update launcher script to respect .stockpile file.

* Thu Jul 7 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.05-2
- Minor spec fixes.

* Thu Jul 7 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.05-1
- Update to latest upstream release.
- 0.43.05 has 64-bit support (in a separate archive); add x86_64 to ExclusiveArch list
- Change "i686" to use the macro for 32-bit x86 architectures

* Tue Jun 21 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.04-1
- Update to latest upstream release.

* Fri Jun 17 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.03-2
- Disable stripping of binaries so dfhack, etc. can recognize DF version

* Fri May 27 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.03-1
- Update to latest upstream release.

* Thu May 12 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.02-1
- Update to latest upstream release.

* Tue May 10 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.01-1
- Update to latest upstream release.

* Wed Feb 10 2016 Ben Rosser <rosser.bjr@gmail.com> 0.42.06-1
- Update to latest upstream release.

* Sat Jan 23 2016 Ben Rosser <rosser.bjr@gmail.com> 0.42.05-3
- Split up dwarffortress rather than bundling it in /opt.
- Dwarf_Fortress binary is in libexecdir, along with compiled libgraphics.
- Data and raws have been moved into datadir.
- The dwarffortress script has been updated to refer to these locations.
- Added README.linux to documentation.

* Mon Jan 18 2016 Ben Rosser <rosser.bjr@gmail.com> 0.42.05-2
- Added explicit requires on alsa-plugins-pulseaudio that RPM failed to find.

* Mon Jan 18 2016 Ben Rosser <rosser.bjr@gmail.com> 0.42.05-1
- Upgraded to latest upstream release.

* Fri Jan  1 2016 Ben Rosser <rosser.bjr@gmail.com> 0.42.04-1
- Initial package, based heavily on the work done for Arch Linux.
