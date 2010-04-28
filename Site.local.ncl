#define YmakeRoot $(DESTDIR)@prefix@
#define ManRoot $(DESTDIR)@mandir@
#define LibRoot $(DESTDIR)@libdir@/ncarg
#define SharePath $(DESTDIR)@datadir@

#define BuildWithF90 TRUE
#define IncSearch -I/usr/include/netcdf -I/usr/include/udunits2
#define LibSearch -L@libdir@/hdf

#define BuildNetCDF4 1
#define NetCDF4lib -lnetcdf
#define BuildV5D 0
#define BuildHDFEOS 0
#define BuildHDFEOS5 0
#define BuildTRIANGLE 0
#define V5Dlib
#define BuildDODS 1
#define HDFlib -lmfhdf -ldf -ljpeg -lz
#define BuildUdunits 1
#define UdUnitslib -ludunits2

