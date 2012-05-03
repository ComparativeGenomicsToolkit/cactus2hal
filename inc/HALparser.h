/*
 * HALparser.h
 *
 *  Created on: May 1, 2012
 *      Author: Vlado Uzunangelov
 */

#ifndef HALPARSER_H_
#define HALPARSER_H_

#include "hal.h"

class HALparser{
public:
	hal::Genome* convertToHALGenome();//this and get Genome size should have the same args
	hal::Alignment* updateHALAlignment();

protected:

	hal_size_t* getGenomeSize();
	void parseOptions(int argc, char **argv, std::string &MAFFilePath,
			std::string &DBPath, std::string &HALAlignmentPath);
};


#endif /* HALPARSER_H_ */
