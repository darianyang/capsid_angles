parm pent-dim1-leap/pent-dim1-leap.pdb
trajin pent-dim1-leap/pent-dim1-leap.pdb

# single monomer vector (H8 and H9 of M1)
vector V1 :18-22@CA,C,O,N :46-49@CA,C,O,N 
# vector with both monomers
vector V2 :18-22@CA,C,O,N :134-137@CA,C,O,N 

# other side
# single monomer vector (H8 and H9 of M2)
vector V3 :106-110@CA,C,O,N :46-49@CA,C,O,N 
# vector with both monomers
vector V4 :106-110@CA,C,O,N :134-137@CA,C,O,N 

# previous c2 angle calc
vector D1 :1-75@CA,C,O,N :39@CA,C,O,N 
vector D2 :89-163@CA,C,O,N :127@CA,C,O,N 

run
writedata pent-dim1-leap/oang_m1.mol2 vectraj V1 V2 trajfmt mol2
writedata pent-dim1-leap/oang_m2.mol2 vectraj V3 V4 trajfmt mol2
writedata pent-dim1-leap/c2ang.mol2 vectraj D1 D2 trajfmt mol2

vectormath vec1 V1 vec2 V2 out pent-dim1-leap/o_angle.dat name o_angle_m1 dotangle
vectormath vec1 V3 vec2 V4 out pent-dim1-leap/o_angle.dat name o_angle_m2 dotangle
vectormath vec1 D1 vec2 D2 out pent-dim1-leap/c2_angle.dat name c2_angle dotangle
go
quit
