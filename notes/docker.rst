================================================================================
Docker Guide
================================================================================

https://docs.docker.com/engine/installation/mac/

.. todo

--------------------------------------------------------------------------------
Installing
--------------------------------------------------------------------------------

.. code-block:: bash

    brew install docker docker-machine
    brew cask install virtualbox
    docker-machine create --driver virtualbox default
    docker-machine start default
    eval $(docker-machine env default)
