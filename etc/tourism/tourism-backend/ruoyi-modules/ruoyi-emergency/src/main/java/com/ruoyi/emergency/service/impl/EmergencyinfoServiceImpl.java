package com.ruoyi.emergency.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.emergency.mapper.EmergencyinfoMapper;
import com.ruoyi.emergency.domain.Emergencyinfo;
import com.ruoyi.emergency.service.IEmergencyinfoService;

/**
 * 应急信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-12
 */
@Service
public class EmergencyinfoServiceImpl implements IEmergencyinfoService 
{
    @Autowired
    private EmergencyinfoMapper emergencyinfoMapper;

    /**
     * 查询应急信息
     * 
     * @param id 应急信息主键
     * @return 应急信息
     */
    @Override
    public Emergencyinfo selectEmergencyinfoById(Long id)
    {
        return emergencyinfoMapper.selectEmergencyinfoById(id);
    }

    /**
     * 查询应急信息列表
     * 
     * @param emergencyinfo 应急信息
     * @return 应急信息
     */
    @Override
    public List<Emergencyinfo> selectEmergencyinfoList(Emergencyinfo emergencyinfo)
    {
        return emergencyinfoMapper.selectEmergencyinfoList(emergencyinfo);
    }

    /**
     * 新增应急信息
     * 
     * @param emergencyinfo 应急信息
     * @return 结果
     */
    @Override
    public int insertEmergencyinfo(Emergencyinfo emergencyinfo)
    {
        return emergencyinfoMapper.insertEmergencyinfo(emergencyinfo);
    }

    /**
     * 修改应急信息
     * 
     * @param emergencyinfo 应急信息
     * @return 结果
     */
    @Override
    public int updateEmergencyinfo(Emergencyinfo emergencyinfo)
    {
        return emergencyinfoMapper.updateEmergencyinfo(emergencyinfo);
    }

    /**
     * 批量删除应急信息
     * 
     * @param ids 需要删除的应急信息主键
     * @return 结果
     */
    @Override
    public int deleteEmergencyinfoByIds(Long[] ids)
    {
        return emergencyinfoMapper.deleteEmergencyinfoByIds(ids);
    }

    /**
     * 删除应急信息信息
     * 
     * @param id 应急信息主键
     * @return 结果
     */
    @Override
    public int deleteEmergencyinfoById(Long id)
    {
        return emergencyinfoMapper.deleteEmergencyinfoById(id);
    }

    @Override
    public int confirmEmergencyinfoByIds(Long[] ids) {
        return emergencyinfoMapper.confirmEmergencyinfoByIds(ids);
    }
}
