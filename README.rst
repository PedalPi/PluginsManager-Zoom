MidiMultistompController
========================

..
  .. image:: https://travis-ci.org/PedalPi/PluginsManager.svg?branch=master
      :target: https://travis-ci.org/PedalPi/PluginsManager
      :alt: Build Status
  .. image:: https://readthedocs.org/projects/pedalpi-pluginsmanager/badge/?version=latest
      :target: http://pedalpi-pluginsmanager.readthedocs.io/?badge=latest
      :alt: Documentation Status
  .. image:: https://codecov.io/gh/PedalPi/PluginsManager/branch/master/graph/badge.svg
      :target: https://codecov.io/gh/PedalPi/PluginsManager
      :alt: Code coverage


Simplified API for effects unit control.

..
   **Documentation:**
      http://pedalpi-pluginsmanager.readthedocs.io/

**Code:**
   https://github.com/PedalPi/PluginsManager

..
   **Python Package Index:**
      https://pypi.org/project/PedalPi-PluginsManager

..
   **License:**
      `Apache License 2.0`_

.. _Apache License 2.0: https://github.com/PedalPi/PluginsManager/blob/master/LICENSE

Installation
------------

Probably PedalPi requirements

.. code::

   sudo apt-get install portaudio19-dev

Examples
--------

Coming soon

Supported Equipment
-------------------

This library extends `PluginsManager`_ to control third effects unit. Note that for this to be possible,
the effects unit must be communicable by some protocol (usually MIDI) and someone in the community must
implement support in this library. These are currently supported devices.
A detailed list of support for each device is below.

.. _PluginsManager: https://github.com/PedalPi/PluginsManager

* Zoom G3 v2
* Zoom MS50G (comming soon)


Zoom G3
~~~~~~~

.. code:: python

   # Instantiate
   zoom = ZoomG3v2()
   # Connect the object 'zoom' with the real equipment
   zoom.connect()

   # Load all patches from the equipment
   zoom.load_data()

   # Disconnect the equipment
   zoom.disconnect()



**Columns:**

* :code:`Command`: Feature
* :code:`Pedalboard`: Information sended by the Zoom G3 equipment
  in the "pedalboard" message data.
  These are usually messages about the state of a pedalboard, but it
  is possible (but not yet verified) that general information about
  the equipment is also passed, such as battery information, global level,
  etc ...
* :code:`Read Change`: Zoom equipment informs a change applied directly in it
* :code:`Send Change`: API informs changes to the Zoom equipment

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
| Tunner on/off     |            | no support  | only API    |
+-------------------+------------+-------------+-------------+
| Tunner+mute on/off|            | no support  | only API    |
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
| USB audio volume  |            | no support  | ?           |
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

* :code:`Blank cells`: Not implemented. It may be supported.
* :code:`x`: Integrated with PluginsManager API
* :code:`only API`: Not yet integrated with PluginsManager API
* :code:`?`: Unknown. Probably not possible
* :code:`no support`: Equipment doesn't informs/receive information about


**Other info:**

* Changes applied by the API are not automatically saved to the device.
* If the autosave option is active on the machine, it eventually saves
  the latest changes. However, changes made may be lost if the connection
  to the equipment is terminated before the autosave saves it.


Zoom MS50g
~~~~~~~~~~

.. code:: python

   # Instantiate
   zoom = ZoomMS50gv3()
   # Connect the object 'zoom' with the real equipment
   zoom.connect()

   # Load all patches from the equipment
   zoom.load_data()

   # Disconnect the equipment
   zoom.disconnect()



**Columns:**

* :code:`Command`: Feature
* :code:`Pedalboard`: Information sended by the Zoom G3 equipment
  in the "pedalboard" message data.
  These are usually messages about the state of a pedalboard, but it
  is possible (but not yet verified) that general information about
  the equipment is also passed, such as battery information, global level,
  etc ...
* :code:`Read Change`: Zoom equipment informs a change applied directly in it
* :code:`Send Change`: API informs changes to the Zoom equipment

+-------------------+------------+-------------+-------------+
|                   | Command                                |
+-------------------+------------+-------------+-------------+
| Command           | Pedalboard | Read Change | Send Change |
+===================+============+=============+=============+
| **Pedalboard/Patch data**                                  |
+-------------------+------------+-------------+-------------+
| Patch Name        | x          | no support  |             |
+-------------------+------------+-------------+-------------+
| Patch Level       | no support                             |
+-------------------+------------+-------------+-------------+
| Patch Display pos |            | no support  |             |
+-------------------+------------+-------------+-------------+
| Effect            |            |             |             |
+-------------------+------------+-------------+-------------+
| Effect status     |            |             |             |
+-------------------+------------+-------------+-------------+
| Param value       |            |             |             |
+-------------------+------------+-------------+-------------+
| CTRL SW/PDL       |            |             |             |
+-------------------+------------+-------------+-------------+
| PDL DST           |            |             |             |
+-------------------+------------+-------------+-------------+
| Swap effects      |            |             |             |
+-------------------+------------+-------------+-------------+
| Set current patch |            |             |             |
+-------------------+------------+-------------+-------------+
| **Tunner**                                                 |
+-------------------+------------+-------------+-------------+
| Tunner on/off     |            |             |             |
+-------------------+------------+-------------+-------------+
| Tunner+mute on/off|            |             |             |
+-------------------+------------+-------------+-------------+
| **Replace/swap**                                           |
+-------------------+------------+-------------+-------------+
| Replace patch     |            |             |             |
+-------------------+------------+-------------+-------------+
| Swap patches      |            |             |             |
+-------------------+------------+-------------+-------------+
| **Global data**                                            |
+-------------------+------------+-------------+-------------+
| Global tempo      |            | conflictTAP |             |
+-------------------+------------+-------------+-------------+
| Global level      | no support                             |
+-------------------+------------+-------------+-------------+
| Global output     | no support                             |
+-------------------+------------+-------------+-------------+
| Signal patch      | no support                             |
+-------------------+------------+-------------+-------------+
| Battery           |            | no support  |             |
+-------------------+------------+-------------+-------------+
| LCD               |            | no support  |             |
+-------------------+------------+-------------+-------------+
| Autosave (on off) |            | no support  |             |
+-------------------+------------+-------------+-------------+
| USB audio volume  | no support                             |
+-------------------+------------+-------------+-------------+
| **Other messages**                                         |
+-------------------+------------+-------------+-------------+
| Get current patch              | no support  |             |
+-------------------+------------+-------------+-------------+
| Change autosaved               |             |             |
+-------------------+------------+-------------+-------------+
| Manual save msg                |             |             |
+-------------------+------------+-------------+-------------+

**Legend:**

* :code:`conflictTAP`: Same message to the 4º effect 7º param value
* :code:`Blank cells`: Not implemented. It may be supported.
* :code:`x`: Integrated with PluginsManager API
* :code:`only API`: Not yet integrated with PluginsManager API
* :code:`?`: Unknown. Probably not possible
* :code:`no support`: Equipment doesn't informs/receive information about
