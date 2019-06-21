#!/bin/bash
killall xed
sudo cp /tmp/hcl.lang /usr/share/gtksourceview-2.0/language-specs/hcl.lang
sudo cp /tmp/hcl.lang /usr/share/gtksourceview-3.0/language-specs/hcl.lang
(xed ~/code/ai/sacrificepress.com/setup-ansible.sh ~/code/ai/sacrificepress.com/main.tf &)
