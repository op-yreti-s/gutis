"""
Functions to convert between OPS object and PyRETIS objects.
"""
import pyretis
import openpathsampling as paths
import simtk.unit as unit
import numpy as np


def ops_box_vectors_to_pyretis(box_vectors):
    """Convert OPS box_vectors (square numpy array) to PyRETIS ``Box``

    Parameters
    ----------
    box_vectors: :class:`numpy.array` shape (n_dim, n_dim)
        input box vectors from OpenPathSampling

    Returns
    -------
    :class:`pyretis.core.Box`
        PyRETIS ``Box`` object for the box vectors
    """
    if isinstance(box_vectors, unit.Quantity):
        box_vectors = box_vectors._value
    for i in range(len(box_vectors)):
        for j in range(len(box_vectors[i])):
            if i != j and box_vectors[i][j] != 0:
                raise ValueError("PyRETIS requires rectangular boxes.")
    box = pyretis.core.Box(size=[[0.0, box_vectors[i, i]]
                                 for i in range(len(box_vectors))])
    return box


def pyretis_box_to_ops(box):
    """Convert PyRETIS ``Box`` to OPS box_vectors (numpy array)
    """
    box_vectors = np.zeros(shape=(box.dim, box.dim))
    for i in range(box.dim):
        box_vectors[i, i] = box.length[i]

    # TODO: may need to add units for OpenMM
    return box_vectors


def ops_snapshot_to_pyretis(snapshot):
    """Convert an OPS ``Snapshot`` to a PyRETIS ``System``

    Parameters
    ----------
    snapshot : :class:`openpathsampling.Snapshot`
        input snapshot

    Returns
    -------
    :class:`pyretis.core.System`
        output system
    """
    box = ops_box_vectors_to_pyretis(snapshot.box_vectors)
    system = pyretis.core.System(box=box)
    load_system_with_snapshot(system, snapshot, update_box=False)
    return system


def load_system_with_snapshot(system, snapshot, update_box=True):
    """Load a PyRETIS ``System`` object with data from an OPS ``Snapshot``
    """
    if update_box:
        box = ops_box_vectors_to_pyretis(snapshot.box_vectors)
        system.box = box

    pos = snapshot.coordinates
    vel = snapshot.velocities

    # strip units if present
    if isinstance(pos, unit.Quantity):
        pos = pos._value
    if isinstance(vel, unit.Quantity):
        vel = vel._value

    particles = pyretis.core.Particles(dim=system.box.dim)
    particles.pos = pos
    particles.vel = vel

    system.particles = particles


def pyretis_system_to_ops(system):
    pass
