#ifndef _ED2K_H_
#define _ED2K_H_

#include <string>
#include <openssl/md4.h>

class Ed2k {
	private:
		MD4_CTX md4_partial;
		MD4_CTX md4_final;
		unsigned int size_total;
		std::string digest_str;
	public:
		Ed2k();
		void update(std::string data);
		std::string digest();
};

#endif // _ED2K_H_
