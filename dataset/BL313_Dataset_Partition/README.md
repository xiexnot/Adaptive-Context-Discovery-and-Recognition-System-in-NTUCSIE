# BL313 Dataset Partition

### Data Source

BL313's dataset with single user's activity

### Data Category

full instances (54082) with full features in separate files (appliance, environment, motion)

### Detailed Data Description

Environment:	livingroom_tempterature	livingroom_humidity	livingroom_luminance	study_tempterature	study_humidity	study_luminance	bedroom_tempterature	bedroom_humidity	bedroom_luminance	kitchen_tempterature	kitchen_humidity	kitchen_luminance	hallway_tempterature	hallway_humidity	hallway_luminance

Appliance:	light_livingroom	audio_livingroom	current_watercoldfan_livingroom	current_TV_livingroom	current_lamp_livingroom	current_xbox_livingroom	current_AC_livingroom	light_study	current_lamp_study	current_NB_study	light_bedroom	current_lamp_bedroom	current_PC_bedroom	current_AC_bedroom	current_nightlamp_bedroom	light_kitchen	current_microwave_kitchen	light_hallway	switch_door_hallway


Motion:	people_livingroom	people_study	people_bedroom	people_kitchen	people_hallway


### Hints

Environment Dataset has been separated. However, this kind of features has not contribution to clustering in BL313
So in the hierarchical discovery, recognition and interactive adaptation (my master thesis), environment features will not be updated and considered.
