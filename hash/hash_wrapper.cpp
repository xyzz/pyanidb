#include "hash.h"

#include <boost/python.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(_hash)
{
	class_<Hash>("Hash")
		.def("update", &Hash::update)
		.def("crc32", &Hash::crc32)
		.def("ed2k", &Hash::ed2k)
		.def("md5", &Hash::md5)
		.def("sha1", &Hash::sha1);
}
