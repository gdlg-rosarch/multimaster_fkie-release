# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Fraunhofer FKIE/US, Alexander Tiderko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Fraunhofer nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import shlex
import subprocess
import threading

import rospy

import node_manager_fkie as nm
from detailed_msg_box import DetailedError
from supervised_popen import SupervisedPopen

class ScreenHandlerException(Exception):
  pass

class ScreenSelectionRequest(Exception):
  ''' '''
  
  def __init__(self, choices, error):
    Exception.__init__(self)
    self.choices = choices
    self.error = error
  
  def __str__(self):
    return "ScreenSelectionRequest from "  + self.choices + "::" + repr(self.error)


class ScreenHandler(object):
  '''
  The class to handle the running screen sessions and create new sessions on 
  start of the ROS nodes.
  '''

  LOG_PATH = os.environ.get('ROS_LOG_DIR') if os.environ.get('ROS_LOG_DIR') else os.path.join(os.path.expanduser('~'), '.ros/log/')
  SCREEN = "/usr/bin/screen"
  SLASH_SEP = '_'
  
  @classmethod
  def createSessionName(cls, node=None):
    '''
    Creates a name for the screen session. All slash separators are replaced by 
    L{SLASH_SEP}
    @param node: the name of the node
    @type node: C{str}
    @return: name for the screen session.
    @rtype: C{str}
    '''
#    package_name = str(package) if not package is None else ''
#    lanchfile_name = str(launchfile).replace('.launch', '') if not launchfile is None else ''
    node_name = str(node).replace('/',cls.SLASH_SEP) if not node is None else ''
#    result = ''.join([node_name, '.', package_name, '.', lanchfile_name])
    return node_name

  @classmethod
  def splitSessionName(cls, session):
    '''
    Splits the screen session name into PID and session name generated by 
    L{createSessionName()}.
    @param session: the screen session name
    @type session: C{str}
    @return: PID, session name generated by L{createSessionName()}. Not presented 
      values are coded as empty strings. Not valid session names have an empty 
      PID string.
    @rtype: C{str, str} 
    '''
    result = session.split('.', 1)
    if len(result) != 2:
      return '', ''
    pid = result[0]
    node = result[1]#.replace(cls.SLASH_SEP, '/')
#    package = result[2]
#    launch = ''.join([result[3], '.launch']) if len(result[2]) > 0 else result[2]
    return pid, node#, package, launch
  
  @classmethod
  def testScreen(cls):
    '''
    Tests for whether the L{SCREEN} binary exists and raise an exception if not.
    @raise ScreenHandlerException: if the screen binary not exists. 
    '''
    if not os.path.isfile(cls.SCREEN):
      raise ScreenHandlerException(''.join([cls.SCREEN, " is missing"]))

  @classmethod
  def getScreenLogFile(cls, session=None, node=None):
    '''
    Generates a log file name for the screen session.
    @param session: the name of the screen session
    @type session: C{str}
    @return: the log file name
    @rtype: C{str}
    '''
    if not session is None:
      return os.path.join(cls.LOG_PATH, session+'.log')
    elif not node is None:
      return os.path.join(cls.LOG_PATH, cls.createSessionName(node)+'.log')
    else:
      return os.path.join(cls.LOG_PATH, 'unknown.log')

  @classmethod
  def getROSLogFile(cls, node):
    '''
    Generates a log file name of the ROS log.
    @param node: the name of the node
    @type node: C{str}
    @return: the ROS log file name
    @rtype: C{str}
    @todo: get the run_id from the ROS parameter server and search in this log folder
    for the log file (handle the node started using a launch file).
    '''
    if not node is None:
      return os.path.join(cls.LOG_PATH, node.strip(rospy.names.SEP).replace(rospy.names.SEP,'_')+'.log')
    else:
      return ''

  @classmethod
  def getScreenCfgFile(cls, session=None, node=None):
    '''
    Generates a configuration file name for the screen session.
    @param session: the name of the screen session
    @type session: C{str}
    @return: the configuration file name
    @rtype: C{str}
    '''
    if not session is None:
      return os.path.join(cls.LOG_PATH, session+'.conf')
    elif not node is None:
      return os.path.join(cls.LOG_PATH, cls.createSessionName(node)+'.conf')
    else:
      return os.path.join(cls.LOG_PATH, 'unknown.conf')

  @classmethod
  def getScreenPidFile(cls, session=None, node=None):
    '''
    Generates a PID file name for the screen session.
    @param session: the name of the screen session
    @type session: C{str}
    @return: the PID file name
    @rtype: C{str}
    '''
    if not session is None:
      return os.path.join(cls.LOG_PATH, session+'.pid')
    elif not node is None:
      return os.path.join(cls.LOG_PATH, cls.createSessionName(node)+'.pid')
    else:
      return os.path.join(cls.LOG_PATH, 'unknown.pid')

  @classmethod
  def getActiveScreens(cls, host, session='', auto_pw_request=True, user=None, pwd=None):
    '''
    Returns the list with all compatible screen names. If the session is set to 
    an empty string all screens will be returned.
    @param host: the host name or IP to search for the screen session.
    @type host: C{str}
    @param session: the name or the suffix of the screen session
    @type session: C{str} (Default: C{''})
    @return: the list with session names
    @rtype: C{[str(session name), ...]}
    @raise Exception: on errors while resolving host
    @see: L{node_manager_fkie.is_local()}
    '''
    try:
      return cls._getActiveScreens(host, session, auto_pw_request, user, pwd)
    except nm.AuthenticationRequest as e:
      raise nm.InteractionNeededError(e, cls.getActiveScreens, (host, session, auto_pw_request))

  @classmethod
  def _getActiveScreens(cls, host, session='', auto_pw_request=True, user=None, pwd=None):
    '''
    Returns the list with all compatible screen names. If the session is set to 
    an empty string all screens will be returned.
    @param host: the host name or IP to search for the screen session.
    @type host: C{str}
    @param session: the name or the suffix of the screen session
    @type session: C{str} (Default: C{''})
    @return: the list with session names
    @rtype: C{[str(session name), ...]}
    @raise Exception: on errors while resolving host
    @see: L{node_manager_fkie.is_local()}
    '''
    output = None
    result = []
    if nm.is_local(host):
      output = cls.getLocalOutput([cls.SCREEN, '-ls'])
    else:
      _, stdout, _, _ = nm.ssh().ssh_exec(host, [cls.SCREEN, ' -ls'], user, pwd, auto_pw_request, close_stdin=True, close_stderr=True)
      output = stdout.read()
      stdout.close()
    if output:
      splits = output.split()
      for i in splits:
        if i.count('.') > 0 and i.endswith(session) and i.find('._') >= 0:
          result.append(i)
    return result


  @classmethod
  def openScreenTerminal(cls, host, screen_name, nodename, user=None):
    '''
    Open the screen output in a new terminal.
    @param host: the host name or ip where the screen is running.
    @type host: C{str}
    @param screen_name: the name of the screen to show
    @type screen_name: C{str}
    @param nodename: the name of the node is used for the title of the terminal
    @type nodename: C{str}
    @raise Exception: on errors while resolving host
    @see: L{node_manager_fkie.is_local()}
    '''
    #create a title of the terminal
#    pid, session_name = cls.splitSessionName(screen_name)
    title_opt = 'SCREEN %s on %s'%(nodename, host)
    if nm.is_local(host):
      cmd = nm.settings().terminal_cmd([cls.SCREEN, '-x', screen_name], title_opt)
      rospy.loginfo("Open screen terminal: %s", cmd)
      SupervisedPopen(shlex.split(cmd), object_id=title_opt, description="Open screen terminal: %s"%title_opt)
    else:
      ps = nm.ssh().ssh_x11_exec(host, [cls.SCREEN, '-x', screen_name], title_opt, user)
      rospy.loginfo("Open remote screen terminal: %s", ps)

  @classmethod
  def openScreen(cls, node, host, auto_item_request=False, user=None, pw=None, items=[]):
    '''
    Searches for the screen associated with the given node and open the screen 
    output in a new terminal.
    @param node: the name of the node those screen output to show
    @type node: C{str}
    @param host: the host name or ip where the screen is running
    @type host: C{str}
    @raise Exception: on errors while resolving host
    @see: L{openScreenTerminal()} or L{_getActiveScreens()}
    '''
    if node is None or len(node) == 0:
      return False
    try:
      if items:
        for item in items:
          #open the selected screen
          cls.openScreenTerminal(host, item, node, user)
      else:
        # get the available screens
        screens = cls._getActiveScreens(host, cls.createSessionName(node), auto_item_request, user, pw)
        if len(screens) == 1:
          cls.openScreenTerminal(host, screens[0], node, user)
        else:
          # create a list to let the user make a choice, which screen must be open
          choices = {}
          for s in screens:
            pid, session_name = cls.splitSessionName(s)
            choices[''.join([session_name, ' [', pid, ']'])] = s
          # Open selection
          if len(choices) > 0:
            if len(choices) == 1:
              cls.openScreenTerminal(host, choices[0], node, user)
            elif auto_item_request:
              from select_dialog import SelectDialog
              items, _ = SelectDialog.getValue('Show screen', '', choices.keys(), False)
              for item in items:
                #open the selected screen
                cls.openScreenTerminal(host, choices[item], node, user)
            else:
              raise ScreenSelectionRequest(choices, 'Show screen')
          else:
            raise DetailedError('Show screen', 'No screen for %s on %s found!\nSee log for details!'%(node, host))
        return len(screens) > 0
    except nm.AuthenticationRequest as e:
      raise nm.InteractionNeededError(e, cls.openScreen, (node, host, auto_item_request))
    except ScreenSelectionRequest as e:
      raise nm.InteractionNeededError(e, cls.openScreen, (node, host, auto_item_request, user, pw))


  @classmethod
  def killScreens(cls, node, host, auto_ok_request=True, user=None, pw=None):
    '''
    Searches for the screen associated with the given node and kill this screens. 
    @param node: the name of the node those screen output to show
    @type node: C{str}
    @param host: the host name or ip where the screen is running
    @type host: C{str}
    '''
    if node is None or len(node) == 0:
      return False
    try:
      # get the available screens
      screens = cls.getActiveScreens(host, cls.createSessionName(node), user=user) #user=user, pwd=pwd
      if screens:
        do_kill = True
        if auto_ok_request:
          from python_qt_binding import QtGui
          result = QtGui.QMessageBox.question(None, "Kill SCREENs?", '\n'.join(screens), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ok)
          if result & QtGui.QMessageBox.Ok:
            do_kill = True
        if do_kill:
          for s in screens:
            pid, _, _ = s.partition('.')
            if pid:
              try:
                nm.starter()._kill_wo(host, int(pid), auto_ok_request, user, pw)
              except:
                import traceback
                rospy.logwarn("Error while kill screen (PID: %s) on host '%s': %s", str(pid), str(host), traceback.format_exc(1))
          if nm.is_local(host):
            SupervisedPopen([cls.SCREEN, '-wipe'], object_id='screen -wipe', description="screen: clean up the socket with -wipe")
          else:
#            output, error, ok = nm.ssh().ssh_exec(host, [cls.SCREEN, '-wipe'])
            nm.ssh().ssh_exec(host, [cls.SCREEN, '-wipe'], close_stdin=True, close_stdout=True, close_stderr=True)
    except nm.AuthenticationRequest as e:
      raise nm.InteractionNeededError(e, cls.killScreens, (node, host, auto_ok_request))

  @classmethod
  def getLocalOutput(cls, cmd):
    '''
    This method is used to read the output of the command executed in a terminal.
    @param cmd: the command to execute in a terminal
    @type cmd: C{str}
    @return: the output generated by the execution of the command.
    @rtype: output
    '''
    ps = SupervisedPopen(cmd, stdout=subprocess.PIPE)
    result = ps.stdout.read()
    return result

  @classmethod
  def getSceenCmd(cls, node):
    '''
    Generates a configuration file and return the command prefix to start the given node
    in a screen terminal.
    @param node: the name of the node
    @type node: C{str}
    @return: the command prefix
    @rtype: C{str}
    '''
    f = open(cls.getScreenCfgFile(node=node), 'w')
    f.write(''.join(["logfile ", cls.getScreenLogFile(node=node), "\n"]))
    f.write("logfile flush 0\n")
    f.write("defscrollback 10000\n")
    ld_library_path = os.getenv('LD_LIBRARY_PATH', '')
    if ld_library_path:
      f.write(' '.join(['setenv', 'LD_LIBRARY_PATH', ld_library_path, "\n"]))
    ros_etc_dir = os.getenv('ROS_ETC_DIR', '')
    if ros_etc_dir:
      f.write(' '.join(['setenv', 'ROS_ETC_DIR', ros_etc_dir, "\n"]))
    f.close()
    return ' '.join([cls.SCREEN, '-c', cls.getScreenCfgFile(node=node), '-L', '-dmS', cls.createSessionName(node=node)])
