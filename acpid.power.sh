#!/bin/sh

PATH=/usr/sbin:/usr/bin

# Check session status using systemd
session_ids=$(loginctl list-sessions 2>/dev/null | awk '{print $1}')
for session in ${session_ids} ; do
	session_status=$(loginctl session-status ${session})
	echo "${session_status}" | grep -e '\(Active: yes\|State: active\)' &> /dev/null &&
		echo "${session_status}" | grep -e '\(gnome-settings-daemon\|cinnamon-settings-daemon\|kded[4-5]\|plasmashell\|xfce4-power-manager\|mate-power-manager\)' &> /dev/null && exit 0
done

# Get the ID of the first active X11 session: using ConsoleKit
uid_session=$(
ck-list-sessions 2>/dev/null | \
awk '
/^Session[0-9]+:$/ { uid = active = x11 = "" ; next }
{ gsub(/'\''/, "", $3) }
$1 == "unix-user" { uid = $3 }
$1 == "active" { active = $3 }
$1 == "x11-display" { x11 = $3 }
active == "TRUE" && x11 != "" {
	print uid
	exit
}')

# Check that there is a power manager, otherwise shut down.
[ "$uid_session" ] &&
ps axo uid,cmd | \
awk '
    $1 == '$uid_session' &&
        ($2 ~ /gnome-power-manager/ || $2 ~ /kpowersave/ ||
        $2 ~ /mate-power-manager/ || $2 ~ /xfce4-power-manager/ ||
        $2 ~ /\/usr\/libexec\/gnome-settings-daemon/ ||
        $2 ~ /\/usr\/libexec\/cinnamon-settings-daemon/ ||
        $2 ~ /kded[4-5]/ || $2 ~ /guidance-power-manager/ ||
        $2 ~ /plasmashell/) \
                { found = 1; exit }
    END { exit !found }
' ||
  shutdown -h now

