#include "ed2k.h"

namespace Hex {
	static char* digits = "0123456789abcdef";
	std::string hex(char* bin, int length) {
		std::string s(length * 2, ' ');
		for(int i = 0; i < length; i++) {
			s[i*2] = digits[(bin[i] >> 4) & 0xf];
			s[i*2+1] = digits[bin[i] & 0xf];
		}
		return s;
	}
	std::string hex(int bin) {
		std::string s(sizeof(int) * 2, ' ');
		for(int i = 0; i < sizeof(int) * 2; i++) {
			s[sizeof(int) * 2 - 1 - i] = digits[bin & 0xf];
			bin = bin >> 4;
		}
		return s;
	}
}

template<class T>
inline T min(T a, T b) {
	return (a > b) ? b : a;
}

Ed2k::Ed2k() {
	MD4_Init(&md4_partial);
	MD4_Init(&md4_final);
	size_total = 0;
	digest_str = "";
}

void Ed2k::update(std::string data_str) {
	unsigned int length = data_str.length();
	const char* data = data_str.c_str();
	while(length) {
		if(!(size_total % (9500 * 1024)) && size_total) {
			unsigned char digest[16];
			MD4_Final(digest, &md4_partial);
			MD4_Update(&md4_final, digest, 16);
			MD4_Init(&md4_partial);
		}
		int size = min<int>(length, (9500 * 1024) - (size_total % (9500 * 1024)));
		MD4_Update(&md4_partial, data, size);
		length -= size;
		data += size;
		size_total += size;
	};
}

std::string Ed2k::digest() {
	if(!digest_str.length()) {
		char* digest = new char[16];
		if(size_total > (9500 * 1024)) {
			unsigned char digest_partial[16];
			MD4_Final(digest_partial, &md4_partial);
			MD4_Update(&md4_final, digest_partial, 16);
			MD4_Final((unsigned char*)digest, &md4_final);
		} else {
			MD4_Final((unsigned char*)digest, &md4_partial);
		}
		digest_str = Hex::hex(digest, 16);
		delete digest;
	}
	return digest_str;
}
