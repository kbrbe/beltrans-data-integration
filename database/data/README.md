This folder is mounted to the blazegraph container.
The `RWStore.properties` file is used to configure blazegraph, among others it defines where blazegraph stores its journal file.
By default this journal file `bigdata.jnl` is also stored in this data directory.

Files in this folder are also available for Blazegraph and thus the bulk dataloader can be used for these files.
Configuration related to the nginx reverse proxy are stored within the `nginx` subfolder
