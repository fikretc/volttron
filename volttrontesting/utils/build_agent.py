import os

import gevent

from volttron.platform import get_home, set_home
from volttron.platform.keystore import KeyStore


def build_agent(platform, identity=None):
    """Builds an agent instance with the passed platform as its bus.

    The agent identity will be set.  If the identity is set to None
    then a random identity will be created.
    """
    set_home()
    agent = platform.build_agent(identity)
    gevent.sleep(0.1) # switch context for a bit
    os.environ.pop('VOLTTRON_HOME')
    return agent


def build_agent_with_key(platform, identity=None):
    """Create an agent instance that has a generated public and private key.

    The passed platform will be the vip-address of the agent and the
     identity will be set.  If the identity is set to None then a random
     identity will be created.
    """
    set_home()
    keys = KeyStore(os.path.join(get_home(),
                                          identity + '.keys'))
    keys.generate()
    agent = platform.build_agent(identity=identity,
                                  serverkey=platform.publickey,
                                  publickey=keys.public,
                                  secretkey=keys.secret)
    # Make publickey easily accessible for these tests
    agent.publickey = keys.public
    gevent.sleep(0.1) # switch context for a bit
    os.environ.pop('VOLTTRON_HOME')
    return agent
