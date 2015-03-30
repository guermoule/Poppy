# -*- coding: utf-8 -*-

import numpy

from functools import partial

#from poppy.creatures import AbstractPoppyCreature

#from .primitives.safe import LimitTorque
#from .primitives.dance import SimpleBodyBeatMotion
#from .primitives.posture import StandPosition, SitPosition
#from .primitives.idle import UpperBodyIdleMotion, HeadIdleMotion
#from .primitives.interaction import ArmsTurnCompliant, PuppetMaster

from Destin_Head_Primitive import Sound_Detect_Motion 

class PoppyHumanoidPart():
    def __init__(self,
                base_path=None, config=None,
                simulator=None, scene=None, host='127.0.0.1', port=19997, id=0,
                use_snap=False, snap_host='0.0.0.0', snap_port=6969,
                sync=True):

		""" Poppy Creature Factory.

        Creates a Robot (real or simulated) and specifies it to make it a specific Poppy Creature.

        :param str config: path to a specific json config (if None uses the default config of the poppy creature - e.g. poppy_humanoid.json)
        :param str simulator: name of the simulator used (only vrep for the moment)
        :param str scene: specify a particular simulation scene (if None uses the default scene of the poppy creature - e.g. poppy_humanoid.ttt)
        :param str host: host of the simulator
        :param int port: port of the simulator
        :param int id: id of robot in the v-rep scene (not used yet!)
        :param bool sync: choose if automatically starts the synchronization loops

        .. warning:: You can not specify a particular config when using a simulated robot!

        """
        if config and simulator:
            raise ValueError('Cannot set a specific config '
                             'when using a simulated version!')

        creature = camelcase_to_underscore(self.__name__)
        base_path = (os.path.dirname(__import__(creature).__file__)
                     if base_path is None else base_path)

        if config is None:
            config = os.path.join(os.path.join(base_path, 'configuration'),
                                  '{}.json'.format(creature))

        if simulator is not None:
            if simulator != 'vrep':
                raise ValueError('Unknown simulation mode: "{}"'.format(simulator))

            from pypot.vrep import from_vrep

            scene_path = os.path.join(base_path, 'vrep-scene')

            if scene is None:
                scene = '{}.ttt'.format(creature)

            if not os.path.exists(scene):
                if ((os.path.basename(scene) != scene) or
                        (not os.path.exists(os.path.join(scene_path, scene)))):
                    raise ValueError('Could not find the scene "{}"!'.format(scene))

                scene = os.path.join(scene_path, scene)

            # TODO: use the id so we can have multiple poppy creatures
            # inside a single vrep scene
            poppy_creature = from_vrep(config, host, port, scene)
            poppy_creature.simulated = True

        else:
            poppy_creature = from_json(config, sync)
            poppy_creature.simulated = False

        if use_snap:
            poppy_creature.snap = SnapRobotServer(poppy_creature, snap_host, snap_port)

        self.setup(poppy_creature)

        return poppy_creature

    @classmethod
    def setup(self, robot):
        robot._primitive_manager._filter = partial(numpy.sum, axis=0)

        if robot.simulated:
            cls.vrep_hack(robot)
        for m in robot.motors:
            m.compliant_behavior = 'safe'
            m.goto_behavior = 'minjerk'
            
        robot.attach_primitive(Sound_Detect_Motion(), 'Head_sound_motion')
        '''
        robot.attach_primitive(StandPosition(robot), 'stand_position')
        robot.attach_primitive(SitPosition(robot), 'sit_position')

        robot.attach_primitive(LimitTorque(robot), 'limit_torque')

        robot.attach_primitive(SimpleBodyBeatMotion(robot, 50), 'dance_beat_motion')

        # robot.limit_torque.start()

        # Idle primitives
        robot.attach_primitive(UpperBodyIdleMotion(robot, 50), 'upper_body_idle_motion')
        robot.attach_primitive(HeadIdleMotion(robot, 50), 'head_idle_motion')

        # Interaction primitives
        robot.attach_primitive(ArmsTurnCompliant(robot, 50), 'arms_turn_compliant')
        robot.attach_primitive(PuppetMaster(robot, 50), 'arms_copy_motion')
        '''
    @classmethod
    def vrep_hack(cls, robot):
        # fix vrep orientation bug
        wrong_motor = [robot.r_knee_y, robot.abs_x, robot.bust_x]

        for m in wrong_motor:
            m.direct = not m.direct
            m.offset = -m.offset