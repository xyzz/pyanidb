#include "ed2k.h"

#include <boost/python.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(_ed2k) {
	class_<Ed2k>("Ed2k")
		.def("update", &Ed2k::update)
		.def("digest", &Ed2k::digest);
}
