Name:           pithos
Version:        0.3.6
Release:        1%{?dist}
Summary:        A Pandora client for the GNOME Desktop

Group:          Applications/File
License:        GPLv3
URL:            http://kevinmehall.net/p/pithos/
# bzr branch lp:pithos pithos-%{version} -r 148
# tar -czf pithos-%{version}.tar.gz pithos-%{version}/
Source0:        pithos-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  python-devel
BuildRequires:  python-distutils-extra

Requires:       dbus-python
Requires:       gstreamer-plugins-bad
Requires:       gstreamer-plugins-good
Requires:       gstreamer-python
Requires:       notify-python
Requires:       pygobject2
Requires:       pygtk2
Requires:       pyxdg

%description
Pithos is a Pandora client for the GNOME Desktop. The official Flash-based
client is a CPU hog, and Pianobar is a great reverse-engineered implementation,
but is command-line only. Neither integrate with the desktop very well, missing
things like media key support and song notifications.

It is recommended that you purchase a Pandora One membership.

%prep
%setup -q
# Copy desktop file before setup.py mangles it
cp %{name}.desktop.in %{name}.desktop
# Fix data path
sed -i 's|../data/|%{_datadir}/%{name}|g' %{name}/pithosconfig.py
# Fix non-executable-script error
sed -i '/^#!\/usr\/bin\/python$/,+1 d' \
    %{name}/plugin.py \
    %{name}/plugins/scrobble.py \
    %{name}/plugins/notification_icon.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --prefix=%{buildroot}%{_prefix}
# Install icon
desktop-file-install --delete-original \
                     --dir %{buildroot}%{_datadir}/applications \
                     --add-only-show-in=GNOME \
                     %{name}.desktop

%files
%defattr(-,root,root,-)
%doc CHANGELOG
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Tue Nov 30 2010 Silas Sewell <silas@sewell.ch> - 0.3.6
- Initial package
