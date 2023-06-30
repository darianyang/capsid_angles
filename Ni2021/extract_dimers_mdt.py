"""
Take multi model PDB and extract CA-CTD dimer PDBs.
"""

import mdtraj
import numpy as np
from tqdm.auto import tqdm
import sys

# load the PDB file with multiple models
#traj = mdtraj.load("Ni2021_models_cut.pdb")
traj = mdtraj.load("Ni2021_models.pdb")
print(traj.n_frames)

# testing distance and compared to chimeraX calc, here is same but in nm
#print(np.linalg.norm(traj_subset[0].xyz - traj_subset[1].xyz))

# note that the Ni2021 structure only has up to V221, not L231
ctd_indices = traj.topology.select("resid 143 to 220")
traj_ctd = traj.atom_slice(ctd_indices)


def dist_between_frames(trajectory, frame_1, frame_2):
    """
    Distance between two trajectory object frames with 1 atom each.
    Returns distance in Angstroms.
    """
    # select only the TRP 184 residue NE1 atoms
    atom_indices = trajectory.topology.select("resname TRP and resid 183 and name NE1")
    frame_1 = frame_1.atom_slice(atom_indices)
    frame_2 = frame_2.atom_slice(atom_indices)
    # calculate the distance between the atom coordinates of the two frames
    distance = np.linalg.norm(frame_1.xyz - frame_2.xyz)
    # convert from nm to Angstroms (1nm = 10A)
    distance *= 10
    return distance

# loop through each frame pair
for i, frame1 in enumerate(tqdm(traj)):
    # only i+ frames to not loop redundant frame pairs
    for j, frame2 in enumerate(traj[i+1:]):
        #print(f"model {i + 1} and {i + 1 + j + 1}")
        # calc distance between the W184 Ne atoms of the frames
        distance = dist_between_frames(traj, frame1, frame2)
        
        # check if the distance is less than 20 A
        if distance < 20:
            # assign model ids for frames 1 and 2
            f1_id = i + 1
            f2_id = i + 1 + j + 1

            # reshape the frame coordinates to ensure compatibility
            # frame1_xyz = frame1.xyz.reshape((1, frame1.n_atoms, 3))
            # frame2_xyz = frame2.xyz.reshape((1, frame2.n_atoms, 3))
            
            # cut frames to only save CTD residues 
            frame1ctd = frame1.atom_slice(ctd_indices)
            frame2ctd = frame2.atom_slice(ctd_indices)
            # make new array or mdtraj trajectory of 2 frames (dimer)
            dimer = np.vstack((frame1ctd.xyz, frame2ctd.xyz))

            # create a new trajectory object with the two frames
            frames_to_save = mdtraj.Trajectory(dimer, topology=traj_ctd.topology)

            # selectively save pent and hex CTD dimers
            # this can be done by comparing the frame numbers to the model # for pents
            # model ids are already assigned as f1_id and f2_id
            # the bottom 60 frames of Ni2021_models are all pentamers
            if f1_id > (traj.n_frames - 60) or f2_id > (traj.n_frames - 60):
                save_dir = "pents"
            else:
                save_dir = "hexs"

            # save the two frames as a single PDB file
            frames_to_save.save_pdb(f"{save_dir}/frames_{f1_id}_{f2_id}.pdb")
            #print(f"saved model {f1_id} and {f2_id} at distance {distance}")
