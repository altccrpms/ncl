#define YmakeRoot $(DESTDIR)@prefix@
#define ManRoot $(DESTDIR)@mandir@
#define LibRoot $(DESTDIR)@libdir@/ncarg
#define SharePath $(DESTDIR)@datadir@

#define BuildWithF90 TRUE
#define IncSearch -I/usr/include/netcdf
#define LibSearch -L@libdir@/hdf

#define BuildUdunits TRUE
#define UdUnitslib
#define BuildV5D FALSE
#define BuildHDFEOS FALSE
#define BuildTRIANGLE 0
#define V5Dlib
#define BuildDODS TRUE
