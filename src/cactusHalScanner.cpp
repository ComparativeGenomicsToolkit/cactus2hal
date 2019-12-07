/*
 * Copyright (C) 2012 by Glenn Hickey (hickey@soe.ucsc.edu)
 *
 * Released under the MIT license, see LICENSE.txt
 */
#include <cassert>
#include <iostream>
#include <stdexcept>
#include <sstream>

#include "cactusHalScanner.h"

using namespace std;
using namespace hal;


CactusHalScanner::CactusHalScanner()
{

}

CactusHalScanner::~CactusHalScanner()
{

}

void CactusHalScanner::scan(const std::string& c2hFilePath)
{
  _c2hFile.open(c2hFilePath.c_str());

  if (!_c2hFile)
  {
    throw runtime_error("error opening path: " + c2hFilePath);
  }
  
  string buffer;
  CactusHalSequence sequenceBuffer;
  CactusHalBottomSegment bsegBuffer;
  CactusHalTopSegment tsegBuffer;

  bool isBottom = false;
  while (!_c2hFile.eof() && _c2hFile.good())
  {
    buffer.clear();
    _c2hFile >> buffer;
    if (buffer == "s")
    {
      _c2hFile >> sequenceBuffer;
      if (!_c2hFile.good())
      {
        throw runtime_error("error parsing sequence " + 
                            sequenceBuffer._name);
      }
      isBottom = sequenceBuffer._isBottom;
      scanSequence(sequenceBuffer);
    }
    else if (buffer == "a")
    {
      if (isBottom == true)
      {
        _c2hFile >> bsegBuffer;
        if (!_c2hFile.good())
        {
          stringstream ss;
          ss << "error parsing bottom segment with name " 
             << bsegBuffer._name << " and start position " 
             << bsegBuffer._start << " in sequence " 
             << sequenceBuffer._name;
          throw runtime_error(ss.str());
        }
        scanBottomSegment(bsegBuffer);
      }
      else
      {
        _c2hFile >> tsegBuffer;
        // don't check errors here for now.  somehow whitespace
        // eater doesn't work all the time, and file gets left in 
        // bad state even when it's ok. 
        scanTopSegment(tsegBuffer);
      }
    }
    else if (buffer.empty() == false)
    {
      throw runtime_error("expected a or s token, got " + buffer);
    }
  }

  scanEndOfFile();  
  _c2hFile.close();
}





