// This is ImHex Pattern Language to parse the picofan protocol.
// 

fn getCommand(u8 cmdByte) {
    if (cmdByte == 1) {
        return "init";
    } else if (cmdByte == 2) {
        return "init ack";
    } else if (cmdByte == 3) {
        return "set";
    } else if (cmdByte == 4) {
        return "get";
    } else {
        return "unknown";
    }
};


fn getType(u8 typeByte) {
    if (typeByte == 1) {
        return "fan";
    } else if (typeByte == 2) {
        return "temp";
    } else {
        return "unknown";
    }
};



// here's where we do the actual highlighting and parsing

u8 msgNum in;
u32 offset = 0x10 * msgNum;

u8 part = 0;



// initialize global out variables

u8 txAddr out;
u8 rxAddr out;

str cmdStr out;
str devType out;
u8 devAddr out;

//init/ack fan
u8 pin_power out;
u8 pin_pwm out;
u8 pin_tach out;

//init/ack temp
u8 pin_onPico out;
u8 pin_onShiftRegister out;

u8 value out;   // value to set or get

u8 checksum out;




// calculate global out variables

//txAddr
u8 txAddrByte @ 0x01 + offset;
txAddr = txAddrByte;

//rxAddr
u8 rxAddrByte @ 0x02 + offset;
rxAddr = rxAddrByte;

//cmdStr
u8 loc_cmdByte = 0x03 + offset;
u8 cmdByte @ loc_cmdByte;
cmdStr = getCommand(cmdByte);

//typeStr
u8 loc_typeByte = 0x04 + offset;
u8 typeByte @ loc_typeByte;
devType = getType(typeByte);

//devAddr
u8 devAddrByte @ 0x05 + offset;
devAddr = devAddrByte;

//command-specific
if ((cmdByte == 1) || (cmdByte == 2)) {     //init/ack
    if (typeByte == 1) {
        //fan
        u8 raw_pin_power @ 0x06 + offset;
        pin_power = raw_pin_power;
        
        u8 raw_pin_pwm @ 0x07 + offset;
        pin_pwm = raw_pin_pwm;
        
        u8 raw_pin_tach @ 0x08 + offset;
        pin_tach = raw_pin_tach;
        
        u8 checksumByte @ 0x09 + offset;
        checksum = checksumByte;
        
    } else if (typeByte == 2) {
        //temp
        u8 raw_pin_onPico @ 0x06 + offset;
        pin_onPico = raw_pin_onPico;
        
        u8 raw_pin_onShiftRegister @ 0x07 + offset;
        pin_onShiftRegister = raw_pin_onShiftRegister;
        
        u8 checksumByte @ 0x08 + offset;
        checksum = checksumByte;
    }
} else if ((cmdByte == 3) || (cmdByte == 4)) {  //get
    //value
    u8 valueByte @ 0x06 + offset;
    value = valueByte;
    
    u8 checksumByte @ 0x07 + offset;
    checksum = checksumByte;
}
