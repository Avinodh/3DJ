import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import Quartz
#import base
from AppKit import NSEvent
#from .base import PyKeyboardMeta, PyKeyboardEventMeta
"""
As the base file, this provides a rough operational model along with the
framework to be extended by each platform.
"""

import time
from threading import Thread


class PyKeyboardMeta(object):
    """
    The base class for PyKeyboard. Represents basic operational model.
    """

    def press_key(self, character=''):
        """Press a given character key."""
        raise NotImplementedError

    def release_key(self, character=''):
        """Release a given character key."""
        raise NotImplementedError

    def tap_key(self, character='', n=1, interval=0):
        """Press and release a given character key n times."""
        for i in range(n):
            self.press_key(character)
            self.release_key(character)
            time.sleep(interval)

    def press_keys(self,characters=[]):
        """Press a given character key."""
        for character in characters:
            self.press_key(character)
        for character in characters:
            self.release_key(character)
    
    def type_string(self, char_string, interval=0):
        """
        A convenience method for typing longer strings of characters. Generates
        as few Shift events as possible."""
        shift = False
        for char in char_string:
            if self.is_char_shifted(char):
                if not shift:  # Only press Shift as needed
                    time.sleep(interval)
                    self.press_key(self.shift_key)
                    shift = True
                #In order to avoid tap_key pressing Shift, we need to pass the
                #unshifted form of the character
                if char in '<>?:"{}|~!@#$%^&*()_+':
                    ch_index = '<>?:"{}|~!@#$%^&*()_+'.index(char)
                    unshifted_char = ",./;'[]\\`1234567890-="[ch_index]
                else:
                    unshifted_char = char.lower()
                time.sleep(interval)
                self.tap_key(unshifted_char)
            else:  # Unshifted already
                if shift and char != ' ':  # Only release Shift as needed
                    self.release_key(self.shift_key)
                    shift = False
                time.sleep(interval)
                self.tap_key(char)

        if shift:  # Turn off Shift if it's still ON
            self.release_key(self.shift_key)

    def special_key_assignment(self):
        """Makes special keys more accessible."""
        raise NotImplementedError

    def lookup_character_value(self, character):
        """
        If necessary, lookup a valid API value for the key press from the
        character.
        """
        raise NotImplementedError

    def is_char_shifted(self, character):
        """Returns True if the key character is uppercase or shifted."""
        if character.isupper():
            return True
        if character in '<>?:"{}|~!@#$%^&*()_+':
            return True
        return False


class PyKeyboardEventMeta(Thread):
    """
    The base class for PyKeyboard. Represents basic operational model.
    """
        modifier_bits = {'Shift': 1,
                     'Lock': 2,
                     'Control': 4,
                     'Mod1': 8,  # X11 dynamic assignment
                     'Mod2': 16,  # X11 dynamic assignment
                     'Mod3': 32,  # X11 dynamic assignment
                     'Mod4': 64,  # X11 dynamic assignment
                     'Mod5': 128,  # X11 dynamic assignment
                     'Alt': 0,
                     'AltGr': 0,  # Uncommon
                     'Caps_Lock': 0,
                     'Command': 0,  # Mac key without generic equivalent
                     'Function': 0,  # Not advised; typically undetectable
                     'Hyper': 0,  # Uncommon?
                     'Meta': 0,  # Uncommon?
                     'Num_Lock': 0,
                     'Mode_switch': 0,  # Uncommon
                     'Shift_Lock': 0,  # Uncommon
                     'Super': 0,  # X11 key, sometimes equivalent to Windows
                     'Windows': 0}  # Windows key, sometimes equivalent to Super

    #Make the modifiers dictionary for individual states, setting all to off
    modifiers = {}
    for key in modifier_bits.keys():
        modifiers[key] = False

    def __init__(self, capture=False):
        Thread.__init__(self)
        self.daemon = True
        self.capture = capture
        self.state = True
        self.configure_keys()

    def run(self):
        self.state = True

    def stop(self):
        self.state = False

    def handler(self):
        raise NotImplementedError

    def tap(self, keycode, character, press):

        pass

    def escape(self, event):
      
        condition = None
        return event == condition

    def configure_keys(self):
       
        pass
# Taken from events.h
# /System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/Headers/Events.h
character_translate_table = {
    'a': 0x00,
    's': 0x01,
    'd': 0x02,
    'f': 0x03,
    'h': 0x04,
    'g': 0x05,
    'z': 0x06,
    'x': 0x07,
    'c': 0x08,
    'v': 0x09,
    'b': 0x0b,
    'q': 0x0c,
    'w': 0x0d,
    'e': 0x0e,
    'r': 0x0f,
    'y': 0x10,
    't': 0x11,
    '1': 0x12,
    '2': 0x13,
    '3': 0x14,
    '4': 0x15,
    '6': 0x16,
    '5': 0x17,
    '=': 0x18,
    '9': 0x19,
    '7': 0x1a,
    '-': 0x1b,
    '8': 0x1c,
    '0': 0x1d,
    ']': 0x1e,
    'o': 0x1f,
    'u': 0x20,
    '[': 0x21,
    'i': 0x22,
    'p': 0x23,
    'l': 0x25,
    'j': 0x26,
    '\'': 0x27,
    'k': 0x28,
    ';': 0x29,
    '\\': 0x2a,
    ',': 0x2b,
    '/': 0x2c,
    'n': 0x2d,
    'm': 0x2e,
    '.': 0x2f,
    '`': 0x32,
    ' ': 0x31,
    '\r': 0x24,
    '\t': 0x30,
    '\n': 0x24,
    'return' : 0x24,
    'tab' : 0x30,
    'space' : 0x31,
    'delete' : 0x33,
    'escape' : 0x35,
    'command' : 0x37,
    'shift' : 0x38,
    'capslock' : 0x39,
    'option' : 0x3A,
    'alternate' : 0x3A,
    'control' : 0x3B,
    'rightshift' : 0x3C,
    'rightoption' : 0x3D,
    'rightcontrol' : 0x3E,
    'function' : 0x3F,
}


# Taken from ev_keymap.h
# http://www.opensource.apple.com/source/IOHIDFamily/IOHIDFamily-86.1/IOHIDSystem/IOKit/hidsystem/ev_keymap.h
special_key_translate_table = {
    'KEYTYPE_SOUND_UP': 0,
    'KEYTYPE_SOUND_DOWN': 1,
    'KEYTYPE_BRIGHTNESS_UP': 2,
    'KEYTYPE_BRIGHTNESS_DOWN': 3,
    'KEYTYPE_CAPS_LOCK': 4,
    'KEYTYPE_HELP': 5,
    'POWER_KEY': 6,
    'KEYTYPE_MUTE': 7,
    'UP_ARROW_KEY': 8,
    'DOWN_ARROW_KEY': 9,
    'KEYTYPE_NUM_LOCK': 10,
    'KEYTYPE_CONTRAST_UP': 11,
    'KEYTYPE_CONTRAST_DOWN': 12,
    'KEYTYPE_LAUNCH_PANEL': 13,
    'KEYTYPE_EJECT': 14,
    'KEYTYPE_VIDMIRROR': 15,
    'KEYTYPE_PLAY': 16,
    'KEYTYPE_NEXT': 17,
    'KEYTYPE_PREVIOUS': 18,
    'KEYTYPE_FAST': 19,
    'KEYTYPE_REWIND': 20,
    'KEYTYPE_ILLUMINATION_UP': 21,
    'KEYTYPE_ILLUMINATION_DOWN': 22,
    'KEYTYPE_ILLUMINATION_TOGGLE': 23
}

class PyKeyboard(PyKeyboardMeta):

    def __init__(self):
      self.shift_key = 'shift'
      self.modifier_table = {'Shift':False,'Command':False,'Control':False,'Alternate':False}
        
    def press_key(self, key):
        if key.title() in self.modifier_table: 
            self.modifier_table.update({key.title():True})
                    
        if key in special_key_translate_table:
            self._press_special_key(key, True)
        else:
            self._press_normal_key(key, True)

    def release_key(self, key):
        # remove the key
        if key.title() in self.modifier_table: self.modifier_table.update({key.title():False})
        
        if key in special_key_translate_table:
            self._press_special_key(key, False)
        else:
            self._press_normal_key(key, False)

    def special_key_assignment(self):
        self.volume_mute_key = 'KEYTYPE_MUTE'
        self.volume_down_key = 'KEYTYPE_SOUND_DOWN'
        self.volume_up_key = 'KEYTYPE_SOUND_UP'
        self.media_play_pause_key = 'KEYTYPE_PLAY'

        # Doesn't work :(
        # self.media_next_track_key = 'KEYTYPE_NEXT'
        # self.media_prev_track_key = 'KEYTYPE_PREVIOUS'

    def _press_normal_key(self, key, down):
        try:
            key_code = character_translate_table[key.lower()]
            # kCGEventFlagMaskAlternate | kCGEventFlagMaskCommand | kCGEventFlagMaskControl | kCGEventFlagMaskShift
            event = Quartz.CGEventCreateKeyboardEvent(None, key_code, down)
            mkeyStr = ''
            for mkey in self.modifier_table:
                if self.modifier_table[mkey]:
                    if len(mkeyStr)>1: mkeyStr = mkeyStr+' ^ '
                    mkeyStr = mkeyStr+'Quartz.kCGEventFlagMask'+mkey                    
            if len(mkeyStr)>1: eval('Quartz.CGEventSetFlags(event, '+mkeyStr+')')
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            if key.lower() == "shift":
              time.sleep(.1)

        except KeyError:
            raise RuntimeError("Key {} not implemented.".format(key))

    def _press_special_key(self, key, down):
        """ Helper method for special keys. 

        Source: http://stackoverflow.com/questions/11045814/emulate-media-key-press-on-mac
        """
        key_code = special_key_translate_table[key]

        ev = NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
                NSSystemDefined, # type
                (0,0), # location
                0xa00 if down else 0xb00, # flags
                0, # timestamp
                0, # window
                0, # ctx
                8, # subtype
                (key_code << 16) | ((0xa if down else 0xb) << 8), # data1
                -1 # data2
            )

        Quartz.CGEventPost(0, ev.Quartz.CGEvent())

class PyKeyboardEvent(PyKeyboardEventMeta):
    def run(self):
        tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,
            Quartz.kCGHeadInsertEventTap,
            Quartz.kCGEventTapOptionDefault,
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown) |
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyUp),
            self.handler,
            None)

        loopsource = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
        loop = Quartz.CFRunLoopGetCurrent()
        Quartz.CFRunLoopAddSource(loop, loopsource, Quartz.kCFRunLoopDefaultMode)
        Quartz.CGEventTapEnable(tap, True)

        while self.state:
            Quartz.CFRunLoopRunInMode(Quartz.kCFRunLoopDefaultMode, 5, False)

    def handler(self, proxy, type, event, refcon):
        key = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        if type == Quartz.kCGEventKeyDown:
            self.press_key(key)
        elif type == Quartz.kCGEventKeyUp:
            self.release_key(key)

        if self.capture:
            Quartz.CGEventSetType(event, Quartz.kCGEventNull)

        return event
        


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        print "Gesture on"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                   
                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                                  
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    k = PyKeyboard()
                    k.press_key('d')
                    k.release_key('d') 
                    #previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    #swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                #print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s, " % (
                        #gesture.id, self.state_names[gesture.state],
                        #circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                k = PyKeyboard()
                k.press_key('e')
                k.release_key('e')
                #print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                        #gesture.id, self.state_names[gesture.state],
                        #swipe.position, swipe.direction, swipe.speed)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                k = PyKeyboard()
                k.press_key('e')
                k.release_key('e')
                #print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        #gesture.id, self.state_names[gesture.state],
                        #keytap.position, keytap.direction )

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                k = PyKeyboard()
                #k.press_key('c')
                #k.release_key(['Command','tab'])
                #print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                        #gesture.id, self.state_names[gesture.state],
                        #screentap.position, screentap.direction )

        #if not (frame.hands.is_empty and frame.gestures().is_empty):
           # print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controlleraaaa
    listener = SampleListener()
    controller = Leap.Controller()

    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
