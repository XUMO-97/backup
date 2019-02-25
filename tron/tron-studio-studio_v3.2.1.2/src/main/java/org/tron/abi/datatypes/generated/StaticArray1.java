package org.tron.abi.datatypes.generated;

import java.util.List;
import org.tron.abi.datatypes.StaticArray;
import org.tron.abi.datatypes.Type;

/**
 * Auto generated code.
 * <p><strong>Do not modifiy!</strong>
 * <p>Please use org.web3j.codegen.AbiTypesGenerator in the 
 * <a href="https://github.com/web3j/web3j/tree/master/codegen">codegen module</a> to update.
 */
public class StaticArray1<T extends Type> extends StaticArray<T> {
    public StaticArray1(List<T> values) {
        super(1, values);
    }

    @SafeVarargs
    public StaticArray1(T... values) {
        super(1, values);
    }
}
