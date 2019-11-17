Probably PedalPi requirements

.. code::

   sudo apt-get install portaudio19-dev


**Columns:**

* Command: Feature
* Pedalboard: Information sended by the Zoom G3 equipment
  in the "pedalboard" message data.
  These are usually messages about the state of a pedalboard, but it
  is possible (but not yet verified) that general information about
  the equipment is also passed, such as battery information, global level,
  etc ...
* Read Change: Zoom equipment informs a change applied directly in it
* Send Change: API informs changes to the Zoom equipment

+-------------------+------------+-------------+-------------+
|                   | Command                                |
+-------------------+------------+-------------+-------------+
| Command           | Pedalboard | Read Change | Send Change |
+===================+============+=============+=============+
| **Pedalboard/Patch data**                                  |
+-------------------+------------+-------------+-------------+
| Patch Name        | x          | x           |             |
+-------------------+------------+-------------+-------------+
| Patch Level       | x          | x           | x           |
+-------------------+------------+-------------+-------------+
| Patch Display pos | ?          | no support  | ?           |
+-------------------+------------+-------------+-------------+
| Effect            | x          | x           | x           |
+-------------------+------------+-------------+-------------+
| Effect status     | x          | x           | x           |
+-------------------+------------+-------------+-------------+
| Param value       | x          | x           | x           |
+-------------------+------------+-------------+-------------+
| CTRL SW/PDL       |            |             |             |
+-------------------+------------+-------------+-------------+
| PDL DST           |            |             |             |
+-------------------+------------+-------------+-------------+
| Swap effects      |            |             | ?           |
+-------------------+------------+-------------+-------------+
| Set current patch | x          | x           | x           |
+-------------------+------------+-------------+-------------+
| **Tunner**                                                 |
+-------------------+------------+-------------+-------------+
| Tunner on/off     |            | no support? | only API    |
+-------------------+------------+-------------+-------------+
| Tunner+mute on/off|            |             | only API    |
+-------------------+------------+-------------+-------------+
| **Replace/swap**                                           |
+-------------------+------------+-------------+-------------+
| Replace patch     |            |             | ?           |
+-------------------+------------+-------------+-------------+
| Swap patches      |            |             | ?           |
+-------------------+------------+-------------+-------------+
| **Global data**                                            |
+-------------------+------------+-------------+-------------+
| Global tempo      |            |             | only API    |
+-------------------+------------+-------------+-------------+
| Global level      |            | no support  | ?           |
+-------------------+------------+-------------+-------------+
| Global output     |            | no support  | ?           |
+-------------------+------------+-------------+-------------+
| Signal patch      |            |             | ?           |
+-------------------+------------+-------------+-------------+
| Battery           |            | no support  | ?           |
+-------------------+------------+-------------+-------------+
| LCD               |            | no support  | ?           |
+-------------------+------------+-------------+-------------+
| Autosave (on off) |            |             | ?           |
+-------------------+------------+-------------+-------------+
| USB audio         |            | no support  | ?           |
+-------------------+------------+-------------+-------------+
| **Other messages**                                         |
+-------------------+------------+-------------+-------------+
| Get current patch              | x           | x           |
+-------------------+------------+-------------+-------------+
| Change autosaved               |             | no support  |
+-------------------+------------+-------------+-------------+
| Manual save msg                |             |             |
+-------------------+------------+-------------+-------------+

**Legend:**

* x: Integrated with PluginsManager API
* no notify: The current version doesn't informs patch name changes
* only API: Not yet integrated with PluginsManager API
* ?: Unknown. Probably not possible
* no support: Equipment doesn't informs/receive information about


**Other info:**

* Changes applied by the API are not automatically saved to the device.
* If the autosave option is active on the machine, it eventually saves
  the latest changes. However, changes made may be lost if the connection
  to the equipment is terminated before the autosave saves it.
