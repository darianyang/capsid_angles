#parm parm.pdb
parm frames_990_1492-leap.pdb
trajin pents.nc

# adjusting all M2 refs by -10 since using 144-221 instead of 144-231 CA-CTD

# single monomer vector (H8 and H9 of M1)
vector V1 :18-22@CA,C,O,N :46-49@CA,C,O,N 
# vector with both monomers
vector V2 :18-22@CA,C,O,N :124-127@CA,C,O,N 

# other side
# single monomer vector (H8 and H9 of M2)
vector V3 :96-100@CA,C,O,N :46-49@CA,C,O,N 
# vector with both monomers
vector V4 :96-100@CA,C,O,N :124-127@CA,C,O,N 

# previous c2 angle calc
vector D1 :1-75@CA,C,O,N :39@CA,C,O,N 
vector D2 :79-153@CA,C,O,N :117@CA,C,O,N 

distance T45-T133 :45&!@CA,C,O,N,H :123&!@CA,C,O,N,H out PENTNC/tt_dist.dat

run
writedata PENTNC/oang_m1.mol2 vectraj V1 V2 trajfmt mol2
writedata PENTNC/oang_m2.mol2 vectraj V3 V4 trajfmt mol2
writedata PENTNC/c2ang.mol2 vectraj D1 D2 trajfmt mol2

vectormath vec1 V1 vec2 V2 out PENTNC/o_angle.dat name o_angle_m1 dotangle
vectormath vec1 V3 vec2 V4 out PENTNC/o_angle.dat name o_angle_m2 dotangle
vectormath vec1 D1 vec2 D2 out PENTNC/c2_angle.dat name c2_angle dotangle
go
quit
