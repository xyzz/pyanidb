#include "ed2k.h"

template<class T>
inline T min(T a, T b) {
	return (a > b) ? b : a;
}

Ed2k::Ed2k() {
	MD4_Init(&md4_partial);
	MD4_Init(&md4_final);
	size_total = 0;
}

void Ed2k::update(const char* data, int length) {
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

char* Ed2k::digest() {
	char* digest = new char[16];
	if(size_total > (9500 * 1024)) {
		unsigned char digest_partial[16];
		MD4_Final(digest_partial, &md4_partial);
		MD4_Update(&md4_final, digest_partial, 16);
		MD4_Final((unsigned char*)digest, &md4_final);
	} else {
		MD4_Final((unsigned char*)digest, &md4_partial);
	}
	return digest;
}
