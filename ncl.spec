Name:           ncl
Version:        5.0.0
Release:        12%{?dist}
Summary:        NCAR Command Language and NCAR Graphics

Group:          Applications/Engineering
License:        BSD
URL:            http://www.ncl.ucar.edu
# You must register for a free account at http://www.earthsystemgrid.org/ before being able to download the source.
Source0:        http://datanode.ucar.edu/data/xserve/ncl/5.0.0/binaries/source/ncl_ncarg_src-5.0.0.tar.gz
Source1:        Site.local.ncl

# ymake uses cpp with some defines on the command line to generate a 
# Makefile which consists in:
#  Template: command line defines
#  Site.conf
#  LINUX
#  Site.conf
#  Template: generic defaults, including default paths
#  Project
#  Rules
#  yMakefile
#  Template: some rules
#
# install paths are set up in Project. Paths used in code are also in 
# Project, in NGENV_DESCRIPT.
Patch0:         ncl-5.0.0-paths.patch
Patch1:         ncarg-4.4.1-deps.patch
Patch2:         ncarg-4.4.2-ppc64.patch
Patch4:         ncl-5.0.0-triangle.patch
Patch5:         ncl-5.0.0-flex.patch
Patch6:         ncl-5.0.0-hdf.patch
Patch7:         ncl-5.0.0-atlas.patch
Patch8:         ncl-5.0.0-png.patch
Patch9:         ncl-5.0.0-wrapit.patch
# don't have the installation target depends on the build target since
# for library it implies running ranlib and modifying the library timestamp
Patch10:        ncl-5.0.0-no_install_dep.patch
# put install and build rules before script rules such that the default rule
# is all
Patch11:        ncl-5.0.0-build_n_scripts.patch
Patch12:        ncl-5.0.0-netcdff.patch
Patch13:        ncl-5.0.0-includes.patch
Patch14:        ncl-5.0.0-uint32.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  /bin/csh, gcc-gfortran, netcdf-devel, hdf-devel >= 4.2r2, libjpeg-devel
BuildRequires:  g2clib-devel, libnc-dap-devel, librx-devel, atlas-devel
# imake needed for makedepend
BuildRequires:  imake, libXt-devel, libXaw-devel, libXext-devel, libXpm-devel
BuildRequires:  byacc, flex

Provides:       ncarg = %{version}-%{release}
Obsoletes:      ncarg < %{version}-%{release}


%description
The NCAR Command Language (NCL) is a free interpreted language designed
specifically for scientific data processing and visualization. NCL has robust
file input and output. It can read and write netCDF-3, netCDF-4 classic (as
of version 4.3.1), HDF4, binary, and ASCII data, and read HDF-EOS2, GRIB1 and
GRIB2 (as of version 4.3.0). The graphics are world class and highly
customizable.

As of version 5.0.0, NCL and NCAR Graphics are released as one package.

The software comes with a couple of useful command line tools:

  * ncl_filedump - prints the contents of supported files (netCDF, HDF,
    GRIB1, GRIB2, HDF-EOS2, and CCM History Tape)
  * ncl_convert2nc - converts one or more GRIB1, GRIB2, HDF and/or HDF-EOS
    files to netCDF formatted files. 


%package devel
Summary:        Development files for NCL and NCAR Graphics
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libXext-devel
Provides:       ncl-static = %{version}-%{release}
Provides:       ncarg-devel = %{version}-%{release}
Obsoletes:      ncarg-devel < %{version}-%{release}

%description devel
%{summary}.


%package examples
Summary:        Example programs and data using NCL
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description examples
Example programs and data using NCL.


%prep
%setup -q -n ncl_ncarg-%{version}
#%patch0 -p1 -b .rpmroot
%patch0 -p1 -b .paths
%patch1 -p1 -b .deps
%patch2 -p1 -b .ppc64
%patch4 -p1 -b .triangle
%patch5 -p1 -b .flex
%patch6 -p1 -b .hdf
%patch7 -p1 -b .atlas
%patch8 -p1 -b .png
%patch9 -p1 -b .wrapit
%patch10 -p1 -b .no_install_dep
%patch11 -p1 -b .build_n_scripts
%patch12 -p1 -b .netcdff
%patch13 -p1 -b .includes
%patch14 -p1 -b .uint32

#Move wrapit.c to wrapit77.c to avoid flex make rule issues
#This works in combination with the wrapit patch
mv ni/src/mkwrap/wrapit.c ni/src/mkwrap/wrapit77.c

#Use ppc config if needed
%ifarch ppc ppc64
cp config/LINUX.ppc32.GNU config/LINUX
%endif

#Fixup LINUX config (to expose vsnprintf prototype)
sed -i -e '/StdDefines/s/-DSYSV/-D_ISOC99_SOURCE/' config/LINUX

#Fixup libdir for atlas lib locations
sed -i -e s,%LIBDIR%,%{_libdir}, config/Project

rm -rf external/blas external/lapack

# fix the install directories
sed -e 's;@prefix@;%{_prefix};' \
 -e 's;@mandir@;%{_mandir};' \
 -e 's;@datadir@;%{_datadir};' \
 -e 's;@libdir@;%{_libdir};' \
 %{SOURCE1} > config/Site.local

pushd ni/src/examples
for file in */*.ncl; do
  sed -i -e 's;load "\$NCARG_ROOT/lib/ncarg/nclex\([^ ;]*\);loadscript(ncargpath("nclex") + "\1);' \
    -e 's;"\$NCARG_ROOT/lib/ncarg/\(data\|database\);ncargpath("\1") + ";' \
   $file
done
popd

%build
# short-cicuit:
./config/ymkmf

# ./config/ymkmf could be also short circuited, since it does:
# (cd ./config; make -f Makefile.ini clean all)
# ./config/ymake -config ./config -Curdir . -Topdir .

#make Build CCOPTIONS="$RPM_OPT_FLAGS -fPIC -Werror-implicit-function-declaration" F77=gfortran F77_LD=gfortran\

make Build CCOPTIONS="$RPM_OPT_FLAGS -fPIC" F77=gfortran F77_LD=gfortran\
 CTOFLIBS="-lgfortran" FCOPTIONS="$RPM_OPT_FLAGS -fPIC -fno-second-underscore -fno-range-check" \
 COPT= FOPT=


%install
rm -rf $RPM_BUILD_ROOT
export NCARG=`pwd`
make install DESTDIR=$RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
#install -m 0644 ncarg.csh ncarg.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
# Don't conflict with allegro-devel (generic API names)
for manpage in $RPM_BUILD_ROOT%{_mandir}/man3/*
do
   manname=`basename $manpage`
   mv $manpage $RPM_BUILD_ROOT%{_mandir}/man3/%{name}_$manname
done
# Remove $RPM_BUILD_ROOT from MakeNcl
#sed -i -e s,$RPM_BUILD_ROOT,,g $RPM_BUILD_ROOT%{_bindir}/MakeNcl


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING Copyright README
#%{_sysconfdir}/profile.d/ncarg.*sh
%{_bindir}/ConvertMapData
%{_bindir}/WriteLineFile
%{_bindir}/WriteNameFile
%{_bindir}/WritePlotcharData
%{_bindir}/cgm2ncgm
%{_bindir}/ctlib
%{_bindir}/ctrans
%{_bindir}/ezmapdemo
%{_bindir}/fcaps
%{_bindir}/findg
%{_bindir}/fontc
%{_bindir}/gcaps
%{_bindir}/graphc
%{_bindir}/ictrans
%{_bindir}/idt
%{_bindir}/med
%{_bindir}/ncargfile
%{_bindir}/ncargpath
%{_bindir}/ncargrun
%{_bindir}/ncargversion
%{_bindir}/ncargworld
%{_bindir}/ncarlogo2ps
%{_bindir}/ncarvversion
%{_bindir}/ncgm2cgm
%{_bindir}/ncgmstat
%{_bindir}/ncl
%{_bindir}/ncl_convert2nc
%{_bindir}/ncl_filedump
%{_bindir}/ncl_grib2nc
%{_bindir}/nnalg
%{_bindir}/pre2ncgm
%{_bindir}/pre2ncgm.prog
%{_bindir}/psblack
%{_bindir}/psplit
%{_bindir}/pswhite
%{_bindir}/pwritxnt
%{_bindir}/ras2ccir601
%{_bindir}/rascat
%{_bindir}/rasgetpal
%{_bindir}/rasls
%{_bindir}/rassplit
%{_bindir}/rasstat
%{_bindir}/rasview
%{_bindir}/tdpackdemo
%{_bindir}/tgks0a
%{_bindir}/tlocal
%dir %{_datadir}/ncarg
%{_datadir}/ncarg/colormaps/
%{_datadir}/ncarg/data/
%{_datadir}/ncarg/database/
%{_datadir}/ncarg/fontcaps/
%{_datadir}/ncarg/graphcaps/
%{_datadir}/ncarg/grib2_codetables/
%{_datadir}/ncarg/nclscripts/
%{_datadir}/ncarg/ngwww/
%{_datadir}/ncarg/sysresfile/
%{_datadir}/ncarg/udunits/
%{_datadir}/ncarg/xapp/
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz
%{_bindir}/scrip_check_input

%files devel
%defattr(-,root,root,-)
%{_bindir}/MakeNcl
%{_bindir}/WRAPIT
%{_bindir}/ncargcc
%{_bindir}/ncargf77
%{_bindir}/ncargf90
%{_bindir}/nhlcc
%{_bindir}/nhlf77
%{_bindir}/nhlf90
%{_bindir}/wrapit77
%{_includedir}/ncarg/
%dir %{_libdir}/ncarg
%{_libdir}/ncarg/libcgm.a
%{_libdir}/ncarg/libfftpack5_dp.a
%{_libdir}/ncarg/libhlu.a
%{_libdir}/ncarg/libncarg.a
%{_libdir}/ncarg/libncarg_c.a
%{_libdir}/ncarg/libncarg_gks.a
%{_libdir}/ncarg/libncarg_ras.a
%{_libdir}/ncarg/libncl.a
%{_libdir}/ncarg/libnclapi.a
%{_libdir}/ncarg/libnio.a
%{_libdir}/ncarg/libngmath.a
%{_libdir}/ncarg/libnfp.a
%{_libdir}/ncarg/libnfpfort.a
%{_libdir}/ncarg/libsphere3.1_dp.a
%{_libdir}/ncarg/ncarg/robj/
%{_mandir}/man3/*.gz

%files examples
%defattr(-,root,root,-)
%{_bindir}/ncargex
%{_bindir}/ng4ex
%{_datadir}/ncarg/examples/
%{_datadir}/ncarg/hluex/
%{_datadir}/ncarg/nclex/
%{_datadir}/ncarg/resfiles/
%{_datadir}/ncarg/tests/
%{_datadir}/ncarg/tutorial/


%changelog
* Thu Sep 11 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-12
- Rebuild for new libdap
- Fix netcdf include location

* Fri Apr 11 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-11
- Add patch to fix raster image problems on non 32-bit platforms
- Add more includes to includes patch

* Thu Mar 27 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-10
- Add patch to fixup some missing includes
- Define _ISOC99_SOURCE to expose vsnprintf prototype
- Update hdf patch to remove hdf/netcdf.h include

* Mon Feb 18 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-9
- Rename Site.local to Site.local.ncl
- Add comment for imake BR

* Wed Feb  6 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-8
- Move examples into separate sub-package

* Fri Feb  1 2008 - Patrice Dumas <pertusus@free.fr> - 5.0.0-7
- put noarch files in datadir
- avoid compilation in %%install

* Mon Jan 14 2008 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-6
- Make BR hdf-devel >= 4.2r2.

* Fri Dec 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-5
- Fixup wrapit flex compilation

* Fri Dec 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-4
- Actually get ncl to build

* Sun Nov 18 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-3
- Move robj to -devel
- Provide ncl-static in ncl-devel
- Turn on BuildUdunits.  Turn off BuildV5D.
- Drop config/LINUX patch, use sed

* Wed Nov 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-2
- Fixup profile.d script permissions, Group, move aed.a to devel

* Tue Nov  6 2007 - Orion Poplawski <orion@cora.nwra.com> - 5.0.0-1
- Initial ncl package, based on ncarg
