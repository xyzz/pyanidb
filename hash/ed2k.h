#ifndef _ED2K_H_
#define _ED2K_H_

#include <openssl/md4.h>

class Ed2k {
	private:
		MD4_CTX md4_partial;
		MD4_CTX md4_final;
		unsigned int size_total;
	public:
		Ed2k();
		void update(const char* data, int length);
		char* digest();
};

#endif // _ED2K_H_
