#define YmakeRoot $(DESTDIR)@prefix@
#define ManRoot $(DESTDIR)@mandir@
#define LibRoot $(DESTDIR)@libdir@/ncarg
#define SharePath $(DESTDIR)@datadir@

#define BuildWithF90 TRUE
#define IncSearch -I/usr/include/netcdf
#define LibSearch -L@libdir@/hdf

#define BuildNetCDF4 0
#define BuildV5D 0
#define BuildHDFEOS 0
#define BuildTRIANGLE 0
#define V5Dlib
#define BuildDODS 1
